"""Hugging Face model loader and inference engine for google/medgemma-1.5-4b-it.
Supports dual-mode execution:
- Local RTX 4050 (6GB): 4-bit NF4 quantization (~2.8GB VRAM)
- Remote A100 (40GB): Native torch.bfloat16 full precision
- Mock Mode: Fast dry-run for local pipeline verification
"""

import os
import re
import json
import torch
from typing import Optional, Dict, Any

try:
    from transformers import (
        AutoProcessor,
        AutoModelForImageTextToText,
        BitsAndBytesConfig
    )
except ImportError:
    AutoProcessor = None
    AutoModelForImageTextToText = None
    BitsAndBytesConfig = None


class MedGemmaEngine:
    """Wrapper for loading and executing inference with google/medgemma-1.5-4b-it."""

    def __init__(
        self,
        model_id: str = "google/medgemma-1.5-4b-it",
        load_in_4bit: Optional[bool] = None,
        mock_mode: bool = False
    ):
        self.model_id = model_id
        self.mock_mode = mock_mode
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Adaptive quantization check based on VRAM
        if load_in_4bit is None:
            if torch.cuda.is_available():
                total_vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                # If GPU memory <= 8GB (e.g. RTX 4050 6GB), use 4-bit
                self.load_in_4bit = total_vram_gb <= 8.0
            else:
                self.load_in_4bit = False
        else:
            self.load_in_4bit = load_in_4bit

    def load_model(self):
        """Initializes processor and loads weights onto target device."""
        if self.mock_mode:
            print("[MedGemmaEngine] Running in MOCK MODE (no model weights loaded).")
            return

        print(f"[MedGemmaEngine] Loading {self.model_id} on {self.device}...")
        hf_token = os.getenv("HF_TOKEN")

        self.processor = AutoProcessor.from_pretrained(
            self.model_id,
            token=hf_token
        )

        model_kwargs = {
            "token": hf_token,
            "device_map": "auto",
            "low_cpu_mem_usage": True
        }

        if self.load_in_4bit and torch.cuda.is_available():
            print("[MedGemmaEngine] Activating 4-bit NF4 quantization for low-VRAM GPU.")
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=False
            )
            model_kwargs["quantization_config"] = quant_config
            model_kwargs["dtype"] = torch.bfloat16
        else:
            print("[MedGemmaEngine] Activating native bfloat16 for high-capacity GPU (A100).")
            model_kwargs["dtype"] = torch.bfloat16

        self.model = AutoModelForImageTextToText.from_pretrained(
            self.model_id,
            **model_kwargs
        )
        print("[MedGemmaEngine] Model successfully loaded.")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 1024,
        temperature: float = 0.1
    ) -> str:
        """Executes clinical reasoning generation given a prompt."""
        if self.mock_mode:
            # Generate deterministic mock clinical differential response
            return json.dumps({
                "primary_diagnosis": "Tuberculosis",
                "differential_diagnoses": ["Tuberculosis", "Histoplasmosis", "Bacterial Pneumonia"],
                "confidence_scores": [0.85, 0.10, 0.05],
                "clinical_rationale": "Patient presented with chronic cough, hemoptysis, and weight loss. Knowledge graph evidence confirmed high co-occurrence with pulmonary tuberculosis."
            }, indent=2)

        if not self.model or not self.processor:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.device)

        # Remove token_type_ids for text-only inputs so Gemma-3 uses standard text masking (compatible with torch 2.5+)
        inputs.pop("token_type_ids", None)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=(temperature > 0.0),
                temperature=temperature if temperature > 0.0 else None
            )

        # Slice off input tokens to get generated output only
        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        return self.processor.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
