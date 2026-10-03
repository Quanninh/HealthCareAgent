"""Qwen2.5-3B-Instruct model loader and execution engine.
Implements:
- Role A: Smart Clinical Entity Extractor (Pre-Retrieval)
- Role B: Diagnostic Reasoner and Baseline Generator
"""

import os
import re
import json
import torch
from typing import Optional, Dict, Any, List

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
except ImportError:
    AutoModelForCausalLM = None
    AutoTokenizer = None
    BitsAndBytesConfig = None

from configs.prompts import (
    ENTITY_EXTRACTION_SYSTEM_PROMPT,
    ENTITY_EXTRACTION_USER_PROMPT
)


class QwenEngine:
    """Loads and manages Qwen2.5-3B-Instruct for extraction and clinical reasoning."""

    def __init__(
        self,
        model_id: str = "Qwen/Qwen2.5-3B-Instruct",
        device: str = "cuda",
        load_in_4bit: bool = True,
        mock_mode: bool = False
    ):
        self.model_id = model_id
        self.device = device if torch.cuda.is_available() else "cpu"
        self.load_in_4bit = load_in_4bit and (self.device == "cuda")
        self.mock_mode = mock_mode
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """Loads tokenizer and 4-bit NF4 quantized model into GPU VRAM."""
        if self.mock_mode:
            print("[QwenEngine] Running in MOCK mode. Model weights will not be loaded.")
            return

        if AutoModelForCausalLM is None:
            raise ImportError("Transformers is not installed. Install via: pip install transformers")

        print(f"[QwenEngine] Loading {self.model_id} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            trust_remote_code=True
        )

        model_kwargs = {
            "device_map": "auto",
            "trust_remote_code": True,
            "low_cpu_mem_usage": True
        }

        if self.load_in_4bit and BitsAndBytesConfig is not None:
            print("[QwenEngine] Activating 4-bit NF4 quantization (~2.2 GB VRAM).")
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=False,
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            model_kwargs["quantization_config"] = quant_config
            model_kwargs["dtype"] = torch.bfloat16
        else:
            model_kwargs["dtype"] = torch.bfloat16 if torch.cuda.is_available() else torch.float32

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            **model_kwargs
        )
        self.model.eval()
        print("[QwenEngine] Qwen2.5-3B-Instruct successfully loaded.")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 1024,
        temperature: float = 0.1
    ) -> str:
        """Executes Role B: Diagnostic Generation given prompt and system instructions."""
        if self.mock_mode:
            return json.dumps({
                "primary_diagnosis": "Tuberculosis",
                "differential_diagnoses": ["Covid19", "Cryptococcosis", "Histoplasmosis"],
                "confidence_scores": [0.85, 0.10, 0.05],
                "clinical_rationale": "Patient presented with chronic cough and hemoptysis, aligning strongly with knowledge graph evidence for Tuberculosis."
            }, indent=2)

        if not self.model or not self.tokenizer:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        text_input = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text_input], return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
                do_sample=(temperature > 0.0),
                temperature=temperature if temperature > 0.0 else None,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_tokens = outputs[0][model_inputs["input_ids"].shape[-1]:]
        return self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    def extract_entities(
        self,
        case_presentation: str,
        canonical_symptoms: Optional[List[str]] = None,
        canonical_labs: Optional[List[str]] = None,
        canonical_visuals: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """Executes Role A: Smart Clinical Entity Extractor."""
        if self.mock_mode:
            return {
                "symptoms": ["cough", "hemoptysis", "weight loss"],
                "labs": ["chest x-ray", "afb smear"],
                "visual_findings": ["cavitary lesion"]
            }

        s_str = ", ".join(canonical_symptoms[:30]) if canonical_symptoms else "common infectious symptoms"
        l_str = ", ".join(canonical_labs[:25]) if canonical_labs else "common laboratory and radiology findings"
        v_str = ", ".join(canonical_visuals[:25]) if canonical_visuals else "common visual pathology terms"

        prompt = ENTITY_EXTRACTION_USER_PROMPT.format(
            case_presentation=case_presentation[:1500],
            canonical_symptoms=s_str,
            canonical_labs=l_str,
            canonical_visuals=v_str
        )

        raw_out = self.generate(
            prompt=prompt,
            system_prompt=ENTITY_EXTRACTION_SYSTEM_PROMPT,
            max_new_tokens=256,
            temperature=0.0
        )

        # Parse extracted entities with fallback
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_out, re.DOTALL)
        json_str = match.group(1) if match else raw_out

        try:
            parsed = json.loads(json_str)
            return {
                "symptoms": [str(s).lower().strip() for s in parsed.get("symptoms", []) if s],
                "labs": [str(l).lower().strip() for l in parsed.get("labs", []) if l],
                "visual_findings": [str(v).lower().strip() for v in parsed.get("visual_findings", []) if v]
            }
        except Exception:
            # Fallback regex extraction of lists
            symptoms = re.findall(r'"symptoms":\s*\[(.*?)\]', raw_out, re.DOTALL)
            labs = re.findall(r'"labs":\s*\[(.*?)\]', raw_out, re.DOTALL)
            s_list = re.findall(r'"([^"]+)"', symptoms[0]) if symptoms else []
            l_list = re.findall(r'"([^"]+)"', labs[0]) if labs else []
            return {
                "symptoms": [s.lower().strip() for s in s_list],
                "labs": [l.lower().strip() for l in l_list],
                "visual_findings": []
            }
