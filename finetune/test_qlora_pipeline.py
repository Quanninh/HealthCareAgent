"""
test_qlora_pipeline.py

Unit test and verification suite for Supervised Fine-Tuning (SFT) using QLoRA.
Tests:
1. SOAP clinical presentation formatting (Subjective + Objective without diagnostic leakage).
2. Dataset loading from sandbox_soap/workspace/core_positive_1500 (ChatML and Alpaca formats).
3. Filtering of unpopulated / empty templates.
4. Completion-only Cross-Entropy loss computation (masking prompt tokens with -100).
5. Deterministic clinical evaluation metrics & ROUGE overlap.
"""

import os
import sys
import unittest

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from finetune.dataset_loader import (
    load_dataset_from_path,
    load_clinical_soap_dataset,
    format_positive_diseases_prompt,
    format_soap_presentation,
    load_soap_record,
    DEFAULT_SOAP_DIR,
    DEFAULT_TRAIN_FILE,
    DEFAULT_TEST_FILE,
    DEFAULT_MANIFEST_FILE
)

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TestQLoRAPipeline(unittest.TestCase):

    def test_soap_presentation_formatting(self):
        """Verifies that format_soap_presentation formats Subjective and Objective cleanly without nulls."""
        sample_soap = {
            "subjective": {
                "chief_complaint": "30-year-old male with 5-day fever.",
                "history_of_present_illness": "Patient developed sudden high fever and joint pain.",
                "past_medical_history": "Travel to endemic area 2 weeks ago.",
                "review_of_systems": None  # Should be omitted cleanly
            },
            "objective": {
                "physical_examination": "Temperature 39 C, maculopapular rash.",
                "routine_investigations": "Platelets 85,000/uL, WBC 3.2 x 10^9/L.",
                "advanced_workup": None  # Should be omitted cleanly
            },
            "assessment_and_plan": {
                "assessment_and_confirmation": "Definitive diagnosis: Dengue fever."
            }
        }

        presentation = format_soap_presentation(sample_soap)
        self.assertIn("[SUBJECTIVE]", presentation)
        self.assertIn("[OBJECTIVE]", presentation)
        self.assertIn("- Chief Complaint: 30-year-old male with 5-day fever.", presentation)
        self.assertIn("- History of Present Illness: Patient developed sudden high fever and joint pain.", presentation)
        self.assertIn("- Past Medical History & Exposures: Travel to endemic area 2 weeks ago.", presentation)
        self.assertNotIn("Review of Systems", presentation)
        self.assertIn("- Physical Examination: Temperature 39 C, maculopapular rash.", presentation)
        self.assertIn("- Routine Investigations: Platelets 85,000/uL, WBC 3.2 x 10^9/L.", presentation)
        self.assertNotIn("Advanced Workup", presentation)

    def test_prompt_formatting(self):
        """
        Verifies that Option B prompts omit candidate target disease hints by default,
        and cleanly include them only when include_candidate_hint=True.
        """
        findings = "[SUBJECTIVE]\n- Chief Complaint: Fever and night sweats."
        q_text = "Which diseases is the patient positive?"

        # Option B (Default: Open deduction with NO candidate disease hint)
        prompt_open = format_positive_diseases_prompt(
            clinical_findings=findings,
            question_text=q_text,
            target_disease="Brucellosis",
            include_candidate_hint=False
        )
        self.assertIn("Which diseases is the patient positive?", prompt_open)
        self.assertNotIn("Candidate Target Disease:", prompt_open)
        self.assertIn("Clinical Presentation (SOAP):", prompt_open)
        self.assertIn("[SUBJECTIVE]", prompt_open)

        # Explicit candidate hint enabled
        prompt_hinted = format_positive_diseases_prompt(
            clinical_findings=findings,
            question_text=q_text,
            target_disease="Brucellosis",
            include_candidate_hint=True
        )
        self.assertIn("Candidate Target Disease: Brucellosis", prompt_hinted)

    def test_dataset_loader_soap_chatml(self):
        """Verifies loading ChatML format from sandbox_soap/workspace/core_positive_1500 (Option B)."""
        ds = load_dataset_from_path(data_path=DEFAULT_SOAP_DIR, format_type="chatml", max_samples=10)

        self.assertEqual(len(ds), 10)
        first_item = ds[0]
        self.assertIn("messages", first_item)
        self.assertEqual(len(first_item["messages"]), 3)
        self.assertEqual(first_item["messages"][0]["role"], "system")
        self.assertEqual(first_item["messages"][1]["role"], "user")
        self.assertEqual(first_item["messages"][2]["role"], "assistant")

        user_content = first_item["messages"][1]["content"]
        self.assertIn("Which diseases is the patient positive?", user_content)
        self.assertIn("Clinical Presentation (SOAP):", user_content)
        # Option B: prompt should NOT leak candidate target disease to user
        self.assertNotIn("Candidate Target Disease:", user_content)

        assistant_content = first_item["messages"][2]["content"]
        self.assertGreater(len(assistant_content), 10)

    def test_dataset_loader_soap_alpaca(self):
        """Verifies loading Alpaca format from sandbox_soap/workspace/core_positive_1500 (Option B)."""
        ds = load_dataset_from_path(data_path=DEFAULT_SOAP_DIR, format_type="alpaca", max_samples=5)

        self.assertEqual(len(ds), 5)
        first_item = ds[0]
        self.assertIn("instruction", first_item)
        self.assertIn("input", first_item)
        self.assertIn("output", first_item)
        self.assertIn("Which diseases is the patient positive?", first_item["instruction"])
        self.assertIn("Clinical Presentation (SOAP):", first_item["input"])
        self.assertNotIn("Candidate Target Disease:", first_item["input"])

    def test_unpopulated_template_filtering(self):
        """Verifies that empty/unpopulated SOAP templates are safely skipped."""
        unpopulated_record = {
            "case_id": "test_empty_01",
            "pair_id": "test_empty_01::Tuberculosis",
            "target_disease": "Tuberculosis",
            "raw_case_text": "A brief text without structured extraction.",
            "soap_note": {
                "subjective": {"chief_complaint": None, "history_of_present_illness": None},
                "objective": {"physical_examination": None},
                "assessment_and_plan": {"assessment_and_confirmation": None}
            }
        }
        res = load_soap_record(unpopulated_record)
        self.assertIsNone(res)

    def test_sft_completion_loss_math(self):
        """
        Validates completion-only Cross-Entropy loss computation:
        - Prompt tokens are masked with -100 (zero loss contribution).
        - Causal shift matches standard Next-Token Prediction for SFT.
        """
        if not TORCH_AVAILABLE:
            self.skipTest("PyTorch is not installed in the local environment.")

        batch_size = 2
        seq_len = 8
        vocab_size = 32

        torch.manual_seed(42)
        logits = torch.randn(batch_size, seq_len, vocab_size, requires_grad=True)

        # Labels: prompt tokens set to -100, completion tokens set to valid token IDs
        labels = torch.full((batch_size, seq_len), -100, dtype=torch.long)
        labels[:, 4:] = torch.randint(0, vocab_size, (batch_size, 4))

        # Causal shift
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        loss = F.cross_entropy(
            shift_logits.view(-1, vocab_size),
            shift_labels.view(-1),
            ignore_index=-100
        )

        self.assertFalse(torch.isnan(loss))
        self.assertGreater(loss.item(), 0.0)

        # Backpropagation check
        loss.backward()
        self.assertIsNotNone(logits.grad)
        self.assertFalse(torch.isnan(logits.grad).any())

        # Tokens before completion (prompt tokens) must have zero gradient
        self.assertTrue(torch.all(logits.grad[:, :3, :] == 0.0))

    def test_parse_clinical_response(self):
        """Verifies parsing and evaluation of Disease Name and ROUGE."""
        from finetune.evaluate_model import parse_clinical_response, compute_rouge_scores

        sample_output = (
            "Definitive diagnosis: Brucellosis (Brucella melitensis infection) with neurobrucellosis. "
            "Confirmation: Brucella antibody titers >1:320. "
            "Treatment & Outcome: Successfully treated with doxycycline and rifampin."
        )
        claims = [{"text": "Brucella antibody titers >1:320", "source": "soap"}]

        parsed = parse_clinical_response(sample_output, "Brucellosis", claims)
        self.assertTrue(parsed["disease_name_correct"])
        self.assertTrue(parsed["disease_in_header"])
        self.assertEqual(parsed["disease_precision"], 1.0)
        self.assertEqual(parsed["disease_recall"], 1.0)
        self.assertEqual(parsed["open_exact_match"], 1.0)
        self.assertEqual(parsed["num_hallucinations"], 0)

        rouge = compute_rouge_scores(sample_output, sample_output)
        self.assertEqual(rouge["rouge1"], 1.0)
        self.assertEqual(rouge["rougeL"], 1.0)

    def test_open_differential_diagnosis_evaluation(self):
        """
        Verifies Option B open differential diagnosis across 15 diseases:
        1. Correct diagnosis with differentials ruled out -> 100% Precision, Recall, EM.
        2. Hallucinating an alternate un-negated disease -> Precision penalty (FP).
        3. Completely wrong disease -> 0% Precision, 0% Recall.
        """
        from finetune.evaluate_model import evaluate_open_differential_diagnosis

        # 1. Gold standard: Target is Brucellosis, differentials ruled out are Malaria and Dengue
        text_correct = (
            "Definitive diagnosis: Brucellosis (Brucella abortus)\n"
            "Confirmatory findings: Blood culture positive for B. abortus.\n"
            "Differentials ruled out: Malaria, Dengue, Typhoid fever negative.\n"
            "Plan: Doxycycline + Streptomycin."
        )
        res1 = evaluate_open_differential_diagnosis(text_correct, "Brucellosis")
        self.assertTrue(res1["target_detected"])
        self.assertEqual(res1["predicted_diseases"], ["brucellosis"])
        self.assertEqual(res1["disease_precision"], 1.0)
        self.assertEqual(res1["disease_recall"], 1.0)
        self.assertEqual(res1["disease_f1"], 1.0)
        self.assertEqual(res1["exact_match"], 1.0)
        self.assertEqual(res1["num_hallucinations"], 0)

        # 2. Hallucination: Target is Dengue, but model also asserts Malaria as positive
        text_hallucination = (
            "The patient is diagnosed with acute Dengue fever and secondary Malaria co-infection. "
            "Both NS1 and blood smear are positive."
        )
        res2 = evaluate_open_differential_diagnosis(text_hallucination, "Dengue")
        self.assertTrue(res2["target_detected"])
        self.assertIn("dengue", res2["predicted_diseases"])
        self.assertIn("malaria", res2["predicted_diseases"])
        self.assertEqual(res2["disease_precision"], 0.5)  # 1 TP / (1 TP + 1 FP)
        self.assertEqual(res2["disease_recall"], 1.0)
        self.assertEqual(res2["exact_match"], 0.0)  # Not exact match due to hallucination
        self.assertEqual(res2["num_hallucinations"], 1)
        self.assertEqual(res2["false_positive_hallucinations"], ["malaria"])

        # 3. Misdiagnosis: Target is Cholera, but model diagnosed Typhoid
        text_wrong = "Definitive diagnosis: Typhoid fever. Blood culture positive for Salmonella typhi."
        res3 = evaluate_open_differential_diagnosis(text_wrong, "Cholera")
        self.assertFalse(res3["target_detected"])
        self.assertEqual(res3["disease_precision"], 0.0)
        self.assertEqual(res3["disease_recall"], 0.0)
        self.assertEqual(res3["exact_match"], 0.0)

    def test_stratified_blind_split_leakage_free(self):
        """
        Verifies the held-out blind test set:
        1. Both train_set.jsonl (698) and blind_test_set.jsonl (125) exist.
        2. Zero case leakage: train_ids & test_ids == empty set.
        3. All 15 diseases are present in the blind test set (stratified coverage).
        4. Manifest exists and confirms leakage-free status.
        """
        import json
        self.assertTrue(os.path.exists(DEFAULT_TRAIN_FILE), f"Missing {DEFAULT_TRAIN_FILE}")
        self.assertTrue(os.path.exists(DEFAULT_TEST_FILE), f"Missing {DEFAULT_TEST_FILE}")
        self.assertTrue(os.path.exists(DEFAULT_MANIFEST_FILE), f"Missing {DEFAULT_MANIFEST_FILE}")

        # Check split manifest
        with open(DEFAULT_MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        meta = manifest.get("metadata", {})
        self.assertTrue(meta.get("disjoint_leakage_free"))
        self.assertEqual(meta.get("total_populated_cases"), 823)
        self.assertEqual(meta.get("total_train_cases"), 698)
        self.assertEqual(meta.get("total_blind_test_cases"), 125)

        # Load train and test sets
        train_records = load_dataset_from_path(split="train")
        test_records = load_dataset_from_path(split="test")
        self.assertEqual(len(train_records), 698)
        self.assertEqual(len(test_records), 125)

        train_ids = set()
        for r in train_records:
            train_ids.add(r.get("case_id"))

        test_ids = set()
        test_diseases = set()
        for r in test_records:
            test_ids.add(r.get("case_id"))
            test_diseases.add(r.get("target_disease"))

        # Zero leakage
        overlap = train_ids.intersection(test_ids)
        self.assertEqual(len(overlap), 0, f"Found data leakage across splits: {overlap}")

        # All 15 diseases represented in blind test set
        expected_diseases = {
            "Brucellosis", "Chikungunya", "Cholera", "COVID-19", "Dengue",
            "Ebola_Filovirus", "HIV_AIDS", "Leishmaniasis", "Leptospirosis",
            "Malaria", "Rabies", "Tuberculosis", "Typhoid_Fever", "Yellow_Fever", "Zika"
        }
        self.assertEqual(test_diseases, expected_diseases)

        # Standardized target_output verification
        for r in test_records:
            self.assertIn("target_output", r)
            self.assertTrue(bool(r["target_output"]))
        for r in train_records:
            self.assertIn("target_output", r)
            self.assertTrue(bool(r["target_output"]))

        # Verify that raw records in train_set.jsonl and blind_test_set.jsonl retain exact sandbox_soap format
        expected_raw_keys = {"case_id", "pair_id", "target_disease", "raw_case_text", "soap_note"}
        with open(DEFAULT_TRAIN_FILE, "r", encoding="utf-8") as f:
            first_train_raw = json.loads(f.readline())
            self.assertEqual(set(first_train_raw.keys()), expected_raw_keys)
            self.assertIn("assessment_and_plan", first_train_raw["soap_note"])

        with open(DEFAULT_TEST_FILE, "r", encoding="utf-8") as f:
            first_test_raw = json.loads(f.readline())
            self.assertEqual(set(first_test_raw.keys()), expected_raw_keys)
            self.assertIn("assessment_and_plan", first_test_raw["soap_note"])

    def test_standardized_target_output_parsing(self):
        """Verifies that load_soap_record extracts target_output from raw SOAP and JSONL formats without conflict."""
        # 1. JSONL format with explicit target_output
        jsonl_rec = {
            "case_id": "PMC12345_01",
            "pair_id": "PMC12345_01::Malaria",
            "target_disease": "Malaria",
            "clinical_presentation": "[SUBJECTIVE]\n- Chief Complaint: Fever.\n\n[OBJECTIVE]\n- Physical Examination: Jaundice.",
            "target_output": "Definitive diagnosis: Malaria. Blood smear positive for Plasmodium falciparum."
        }
        parsed1 = load_soap_record(jsonl_rec)
        self.assertIsNotNone(parsed1)
        self.assertEqual(parsed1["target_output"], jsonl_rec["target_output"])
        self.assertEqual(parsed1["clinical_presentation"], jsonl_rec["clinical_presentation"])

        # 2. Backward compatibility with legacy gt_reasoning / ground_truth_reasoning
        legacy_rec = {
            "case_id": "PMC12345_02",
            "pair_id": "PMC12345_02::Dengue",
            "target_disease": "Dengue",
            "clinical_presentation": "[SUBJECTIVE]\n- Chief Complaint: Severe headache.",
            "ground_truth_reasoning": "Definitive diagnosis: Dengue fever. Confirmed by NS1 antigen."
        }
        parsed2 = load_soap_record(legacy_rec)
        self.assertIsNotNone(parsed2)
        self.assertEqual(parsed2["target_output"], legacy_rec["ground_truth_reasoning"])


if __name__ == "__main__":
    unittest.main()
