"""
index_review_queue.py: Count and index entities directly in human_review_queue.json.

Features:
  1. Counts total entities, unique case IDs, and breakdown by expert decision status.
  2. Injects 'index' (1, 2, 3...) and 'review_id' ('REV_00001'...) into each record.
  3. Reorders keys so 'index' and 'review_id' appear first for clear readability.
  4. Saves directly back to human_review_queue.json in-place (with backup option).
"""

import os
import sys
import json
import argparse
import shutil
from collections import Counter


def count_and_index_review_queue(
    file_path: str = "human_review_queue.json",
    create_backup: bool = True,
    dry_run: bool = False,
) -> dict:
    """
    Count and index entities directly on the specified review queue file.
    
    Args:
        file_path: Path to human_review_queue.json.
        create_backup: If True, creates a .bak copy before modifying.
        dry_run: If True, only prints statistics without modifying the file.
        
    Returns:
        dict containing summary statistics.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        sys.exit(1)

    print(f"Loading '{file_path}'...")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"Error: Expected a JSON array of entities, got {type(data).__name__}")
        sys.exit(1)

    total_count = len(data)
    unique_cases = len(set(item.get("case_id") for item in data if "case_id" in item))
    statuses = Counter(item.get("expert_decision", "PENDING") for item in data)

    print("\n" + "=" * 60)
    print("  HUMAN REVIEW QUEUE: SUMMARY STATISTICS")
    print("=" * 60)
    print(f"  Total Entities:        {total_count:,}")
    print(f"  Unique Patient Cases:  {unique_cases:,}")
    print("\n  Decision Breakdown:")
    for status, count in statuses.items():
        pct = (count / total_count * 100) if total_count else 0
        print(f"    - {status:<15} {count:>8,} ({pct:5.1f}%)")
    print("=" * 60)

    if dry_run:
        print("\n[Dry Run] No changes written to disk.")
        return {
            "total_entities": total_count,
            "unique_cases": unique_cases,
            "statuses": dict(statuses),
        }

    # Backup original file before writing
    if create_backup:
        backup_path = f"{file_path}.bak"
        shutil.copyfile(file_path, backup_path)
        print(f"\nCreated backup copy at '{backup_path}'.")

    # Index each entity and place 'index' and 'review_id' at the front
    indexed_data = []
    pad_width = max(5, len(str(total_count)))  # e.g., REV_00001 or REV_000001

    for idx, item in enumerate(data, start=1):
        record = {
            "index": idx,
            "review_id": f"REV_{idx:0{pad_width}d}",
        }
        # Copy remaining keys, avoiding duplicate index/review_id
        for key, value in item.items():
            if key not in ("index", "review_id"):
                record[key] = value

        indexed_data.append(record)

    # Save back to file in-place
    print(f"Writing {len(indexed_data):,} indexed entities to '{file_path}'...")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(indexed_data, f, indent=4)

    print(f"Successfully indexed '{file_path}' (Index range: 1 to {total_count:,}).\n")

    return {
        "total_entities": total_count,
        "unique_cases": unique_cases,
        "statuses": dict(statuses),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Count and index entities directly in human_review_queue.json."
    )
    parser.add_argument(
        "--file",
        "-f",
        default="human_review_queue.json",
        help="Path to review queue file (default: human_review_queue.json)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a .bak backup file before overwriting",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print count statistics only without modifying the file",
    )

    args = parser.parse_args()

    count_and_index_review_queue(
        file_path=args.file,
        create_backup=not args.no_backup,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
