#!/usr/bin/env python3
import json
import glob
import os
import re
import sys

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "workspace", "core_positive_1500"))

EXPECTED_TOP_KEYS = {"case_id", "pair_id", "target_disease", "raw_case_text", "soap_note"}
EXPECTED_SECTIONS = {"subjective", "objective", "assessment_and_plan"}
EXPECTED_FIELDS = {
    "subjective": {"chief_complaint", "history_of_present_illness", "past_medical_history", "review_of_systems"},
    "objective": {"physical_examination", "routine_investigations", "advanced_workup"},
    "assessment_and_plan": {"assessment_and_confirmation"}
}

FORBIDDEN_STRING_VALUES = {"n/a", "none", "not mentioned", "not stated", "unknown", "null", "nil"}

# Phrases that strongly indicate confirmatory diagnostic leakage into Subjective or Objective
LEAKAGE_PATTERNS = [
    re.compile(r'\bblood culture grew\b', re.I),
    re.compile(r'\bculture confirmed\b', re.I),
    re.compile(r'\bpcr confirmed\b', re.I),
    re.compile(r'\bconfirmed case of\b', re.I),
    re.compile(r'\bdefinitive diagnosis of\b', re.I),
    re.compile(r'\bisolated from blood culture\b', re.I),
    re.compile(r'\bmicrobiologically confirmed\b', re.I),
]

def validate_case(file_path):
    errors = []
    warnings = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"JSON parse error: {e}"], []

    # Check top-level keys
    missing_top = EXPECTED_TOP_KEYS - set(data.keys())
    if missing_top:
        errors.append(f"Missing top-level keys: {missing_top}")

    soap = data.get("soap_note")
    if not isinstance(soap, dict):
        return False, ["'soap_note' is not a dictionary"], []

    missing_sections = EXPECTED_SECTIONS - set(soap.keys())
    if missing_sections:
        errors.append(f"Missing soap sections: {missing_sections}")

    is_populated = False

    for section, fields in EXPECTED_FIELDS.items():
        sec_dict = soap.get(section)
        if not isinstance(sec_dict, dict):
            errors.append(f"Section '{section}' is not a dictionary")
            continue
        
        missing_fields = fields - set(sec_dict.keys())
        if missing_fields:
            errors.append(f"Section '{section}' missing fields: {missing_fields}")
            
        extra_fields = set(sec_dict.keys()) - fields
        if extra_fields:
            errors.append(f"Section '{section}' has unexpected fields: {extra_fields}")

        for fld in fields:
            val = sec_dict.get(fld)
            if val is not None:
                if not isinstance(val, str):
                    errors.append(f"Field '{section}.{fld}' must be string or null, got {type(val).__name__}")
                else:
                    is_populated = True
                    cleaned_val = val.strip().lower()
                    if cleaned_val in FORBIDDEN_STRING_VALUES:
                        errors.append(f"Field '{section}.{fld}' has placeholder string '{val}' instead of null")

    # Anti-leakage checks on Subjective and Objective
    if is_populated:
        subj = soap.get("subjective", {})
        cc = subj.get("chief_complaint") or ""
        hpi = subj.get("history_of_present_illness") or ""
        
        for pat in LEAKAGE_PATTERNS:
            if pat.search(cc):
                warnings.append(f"Potential leakage in chief_complaint: matched '{pat.pattern}'")
            if pat.search(hpi):
                warnings.append(f"Potential leakage in history_of_present_illness: matched '{pat.pattern}'")

    return is_populated, errors, warnings

def main():
    files = sorted(glob.glob(os.path.join(WORKSPACE_DIR, "**", "*.json"), recursive=True))
    case_files = [f for f in files if not f.endswith("manifest.json")]

    total = len(case_files)
    populated = 0
    valid = 0
    failed = 0
    warnings_total = 0

    disease_stats = {}

    for fpath in case_files:
        fname = os.path.basename(fpath)
        parts = fname.replace(".json", "").split("__")
        disease = parts[1] if len(parts) > 1 else "Unknown"

        if disease not in disease_stats:
            disease_stats[disease] = {"total": 0, "populated": 0, "valid": 0, "failed": 0}
        disease_stats[disease]["total"] += 1

        is_pop, errs, warns = validate_case(fpath)
        if is_pop:
            populated += 1
            disease_stats[disease]["populated"] += 1
            if errs:
                failed += 1
                disease_stats[disease]["failed"] += 1
                print(f"[FAIL] {fname}:")
                for e in errs:
                    print(f"  - Error: {e}")
            else:
                valid += 1
                disease_stats[disease]["valid"] += 1
            if warns:
                warnings_total += len(warns)
                for w in warns:
                    print(f"  - Warning [{fname}]: {w}")

    print("=" * 60)
    print("SOAP NOTES VALIDATION REPORT")
    print("=" * 60)
    print(f"Total Cases:     {total}")
    print(f"Populated:       {populated} ({populated/total*100:.1f}%)")
    print(f"Valid & Passing: {valid}")
    print(f"Failed / Errors: {failed}")
    print(f"Warnings:        {warnings_total}")
    print("-" * 60)
    print(f"{'Disease':<20} | {'Total':<6} | {'Populated':<10} | {'Valid':<6}")
    print("-" * 60)
    for d, st in sorted(disease_stats.items()):
        print(f"{d:<20} | {st['total']:<6} | {st['populated']:<10} | {st['valid']:<6}")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
