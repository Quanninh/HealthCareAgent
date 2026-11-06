"""
test_qlora_pipeline.py

Unit test and verification suite for Supervised Fine-Tuning (SFT) using QLoRA.
Tests:
1. Dataset loading from ground_truth_reasoning_all.jsonl (offline-distilled dataset).
2. Prompt construction instructing model to answer: "Which diseases is the patient positive?"
3. Completion-only Cross-Entropy loss computation (masking prompt tokens with -100).
4. Deterministic clinical verdict extraction and ROUGE evaluation metrics.
"""

import sys
import unittest

from finetune.dataset_loader import (
    load_gt_reasoning_dataset,
    format_positive_diseases_prompt
)

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TestQLoRAPipeline(unittest.TestCase):

    def test_prompt_formatting(self):
        """Verifies that the prompt explicitly asks the required question."""
        disease = "Brucellosis"
        findings = "- Test finding 1\n- Test finding 2"
        q_text = "Which diseases is the patient positive?"

        prompt = format_positive_diseases_prompt(disease, findings, q_text)
        self.assertIn("Which diseases is the patient positive?", prompt)
        self.assertIn("Candidate Target Disease: Brucellosis", prompt)
        self.assertIn("- Test finding 1", prompt)

    def test_dataset_loader_chatml(self):
        """Verifies loading ChatML format from ground_truth_reasoning_all.jsonl."""
        gt_file = "gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl"
        ds = load_gt_reasoning_dataset(gt_file=gt_file, format_type="chatml", max_samples=5)

        self.assertEqual(len(ds), 5)
        first_item = ds[0]
        self.assertIn("messages", first_item)
        self.assertEqual(len(first_item["messages"]), 3)
        self.assertEqual(first_item["messages"][0]["role"], "system")
        self.assertEqual(first_item["messages"][1]["role"], "user")
        self.assertEqual(first_item["messages"][2]["role"], "assistant")

        user_content = first_item["messages"][1]["content"]
        self.assertIn("Which diseases is the patient positive?", user_content)

    def test_dataset_loader_alpaca(self):
        """Verifies loading Alpaca format from ground_truth_reasoning_all.jsonl."""
        gt_file = "gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl"
        ds = load_gt_reasoning_dataset(gt_file=gt_file, format_type="alpaca", max_samples=5)

        self.assertEqual(len(ds), 5)
        first_item = ds[0]
        self.assertIn("instruction", first_item)
        self.assertIn("input", first_item)
        self.assertIn("output", first_item)
        self.assertIn("Which diseases is the patient positive?", first_item["instruction"])

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

        # Tokens before the completion (prompt tokens) must have zero gradient
        # Since shift_labels[:, :3] == -100, logits[:, :3, :] should not receive loss gradients
        self.assertTrue(torch.all(logits.grad[:, :3, :] == 0.0))

    def test_parse_clinical_response(self):
        """Verifies parsing and evaluation of Disease Name, Structured Reasoning, and Determination."""
        from finetune.evaluate_model import parse_clinical_response, compute_rouge_scores

        sample_output = (
            "Brucellosis (Brucella abortus / Brucella melitensis infection). "
            "Reasoning: (1) Prolonged fever and unpasteurized dairy exposure. "
            "(2) Positive serology. -> POSITIVE diagnosis confirmed."
        )
        claims = [{"text": "unpasteurized dairy exposure"}, {"text": "Positive serology"}]

        parsed = parse_clinical_response(sample_output, "Brucellosis", claims)
        self.assertTrue(parsed["disease_name_correct"])
        self.assertTrue(parsed["disease_in_header"])
        self.assertTrue(parsed["has_subtype"])
        self.assertTrue(parsed["has_structured_reasoning"])
        self.assertEqual(parsed["num_reasoning_steps"], 2)
        self.assertGreater(parsed["claim_coverage_rate"], 0.0)
        self.assertTrue(parsed["determination_correct"])
        self.assertTrue(parsed["joint_success"])

        rouge = compute_rouge_scores(sample_output, sample_output)
        self.assertEqual(rouge["rouge1"], 1.0)
        self.assertEqual(rouge["rougeL"], 1.0)

    def test_model_comparison_analytics(self):
        """Verifies comparative analytics calculation between Base and Fine-Tuned models on Disease Name + Reason."""
        from finetune.evaluate_model import (
            parse_clinical_response,
            aggregate_clinical_evaluation_metrics,
            compute_model_comparison,
            compute_rouge_scores
        )

        target_dis = "Brucellosis"
        gt_reasoning = (
            "Brucellosis (Brucella abortus infection). Reasoning: (1) Fever with unpasteurized dairy consumption. "
            "(2) Rose Bengal test positive. -> POSITIVE diagnosis confirmed."
        )

        base_resp = "The patient has a systemic fever and requires broad antibiotics."
        ft_resp = gt_reasoning

        claims = [{"text": "unpasteurized dairy consumption"}, {"text": "Rose Bengal test positive"}]

        b_parsed = parse_clinical_response(base_resp, target_dis, claims)
        ft_parsed = parse_clinical_response(ft_resp, target_dis, claims)

        b_records = [{
            "pair_id": "c1", "target_disease": target_dis,
            "parsed": b_parsed, "rouge": compute_rouge_scores(base_resp, gt_reasoning)
        }]
        ft_records = [{
            "pair_id": "c1", "target_disease": target_dis,
            "parsed": ft_parsed, "rouge": compute_rouge_scores(ft_resp, gt_reasoning)
        }]

        b_metrics = aggregate_clinical_evaluation_metrics(b_records)
        ft_metrics = aggregate_clinical_evaluation_metrics(ft_records)

        comp = compute_model_comparison(b_metrics, ft_metrics, b_records, ft_records)

        # Base failed both disease naming and reasoning; Fine-Tuned succeeded
        self.assertEqual(b_metrics["overall_joint_accuracy"]["joint_success_rate"], 0.0)
        self.assertEqual(ft_metrics["overall_joint_accuracy"]["joint_success_rate"], 1.0)
        self.assertEqual(comp["case_transitions"]["ft_improved_count"], 1)
        self.assertEqual(comp["case_transitions"]["net_diagnostic_gain"], 1)


if __name__ == "__main__":
    unittest.main()
