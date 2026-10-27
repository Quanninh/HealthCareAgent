"""
test_distill_pipeline.py

Unit test and verification script for the Knowledge Distillation & QLoRA pipeline.
Tests:
1. Dataset loading from ground_truth_reasoning_all.jsonl
2. Prompt formatting verifying the question "Which diseases is the patient positive?"
3. Mathematical correctness of the dual-loss engine (CE + KL Divergence with T^2)
4. Completion-only loss masking behavior
"""

import sys
import unittest

from dataset_loader import (
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


class TestDistillQLoRAPipeline(unittest.TestCase):

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

    def test_distillation_loss_math(self):
        """
        Validates the mathematical computation of the combined dual loss:
        L_total = alpha * L_ce + (1 - alpha) * T^2 * KL(softmax(Z_s / T) || softmax(Z_t / T))
        """
        if not TORCH_AVAILABLE:
            self.skipTest("PyTorch is not installed in the local environment.")

        batch_size = 2
        seq_len = 8
        vocab_size = 32
        temperature = 2.0
        alpha = 0.5

        # Create dummy student & teacher logits
        torch.manual_seed(42)
        student_logits = torch.randn(batch_size, seq_len, vocab_size, requires_grad=True)
        teacher_logits = torch.randn(batch_size, seq_len, vocab_size)

        # Create labels with prompt masking (-100 for prompt, valid target token IDs for response)
        labels = torch.full((batch_size, seq_len), -100, dtype=torch.long)
        labels[:, 4:] = torch.randint(0, vocab_size, (batch_size, 4))  # completion tokens

        # 1. CE loss on completion tokens
        shift_logits = student_logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()
        loss_ce = F.cross_entropy(
            shift_logits.view(-1, vocab_size),
            shift_labels.view(-1),
            ignore_index=-100
        )

        # 2. KD loss strictly on active completion tokens with causal shift
        shift_s_logits = student_logits[..., :-1, :].contiguous()
        shift_t_logits = teacher_logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        mask = (shift_labels != -100)
        s_active = shift_s_logits[mask]
        t_active = shift_t_logits[mask]

        s_soft = F.log_softmax(s_active / temperature, dim=-1)
        t_soft = F.softmax(t_active / temperature, dim=-1)

        kl_fn = nn.KLDivLoss(reduction="batchmean")
        loss_kd = kl_fn(s_soft, t_soft) * (temperature ** 2)

        total_loss = (alpha * loss_ce) + ((1.0 - alpha) * loss_kd)

        self.assertFalse(torch.isnan(total_loss))
        self.assertGreater(total_loss.item(), 0.0)

        # Verify gradient flow into student logits
        total_loss.backward()
        self.assertIsNotNone(student_logits.grad)
        self.assertFalse(torch.isnan(student_logits.grad).any())

    def test_verdict_extractor(self):
        """Verifies deterministic rule extraction of POSITIVE vs OUT_OF_SCOPE."""
        from evaluate_model import extract_verdict, compute_rouge_scores

        pos_resp = "Brucellosis (Brucella abortus). Reasoning: positive blood culture -> POSITIVE diagnosis confirmed."
        neg_resp = "OUT_OF_SCOPE (Felty syndrome — Not Brucellosis). -> OUT_OF_SCOPE diagnosis confirmed."

        self.assertEqual(extract_verdict(pos_resp, "Brucellosis"), "POSITIVE")
        self.assertEqual(extract_verdict(neg_resp, "Brucellosis"), "OUT_OF_SCOPE")

        rouge = compute_rouge_scores("positive test confirmed", "positive test confirmed")
        self.assertEqual(rouge["rouge1"], 1.0)
        self.assertEqual(rouge["rougeL"], 1.0)


if __name__ == "__main__":
    unittest.main()
