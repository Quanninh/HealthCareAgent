#!/usr/bin/env python3
"""
sandbox/build_prompts.py: MultiCaRe Prompt Generation Runner.
Delegates prompt construction to OOP clinical_data.curation.ClinicalPromptBuilder.
Ensures 100% self-contained schemas, valid documentation paths, and zero legacy references.

Usage:
    python3 sandbox/build_prompts.py --pool labeled_pool
    python3 sandbox/build_prompts.py --pool tier3_pool
"""
import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from clinical_data.curation import ClinicalPromptBuilder


def main():
    parser = argparse.ArgumentParser(description="Generate prompt markdown files for an annotation pool.")
    parser.add_argument(
        "--pool",
        type=str,
        required=True,
        choices=["labeled_pool", "tier3_pool"],
        help="Target pool name ('labeled_pool' or 'tier3_pool')",
    )
    args = parser.parse_args()

    pool_dir = SCRIPT_DIR / "workspace" / args.pool
    manifest_path = pool_dir / "coordinator_manifest.json"
    if not manifest_path.exists():
        print(f"Error: manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(1)

    builder = ClinicalPromptBuilder(workspace_root=PACKAGE_ROOT.parent.parent)
    generated = builder.generate_all_prompts(pool=args.pool, pool_dir=pool_dir)

    print(f"Generated {len(generated)} prompt files in {pool_dir / 'prompts'}:")
    for p in generated:
        print(f"  - {p.relative_to(PACKAGE_ROOT)}")


if __name__ == "__main__":
    main()
