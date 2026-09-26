#!/usr/bin/env python3
"""
Test Native MedRAG integration with the new Payloads corpus.
Verifies DocExtracter and corpus resolution inside MedRAG.
"""

import os
import sys
from pathlib import Path

# Add MedRAG source path
medrag_src = str(Path(__file__).resolve().parent / "MedRAG" / "src")
if medrag_src not in sys.path:
    sys.path.insert(0, medrag_src)

# pyrefly: ignore [missing-import]
from utils import DocExtracter, corpus_names

# Inject custom corpus at runtime without modifying MedRAG source code
corpus_names["Payloads"] = ["payloads"]

def test_payloads_native_integration():
    print("--- Testing MedRAG Native Corpus Integration ---")
    print(f"Registered corpus_names in utils: {list(corpus_names.keys())}")
    assert "Payloads" in corpus_names, "Payloads must be registered in corpus_names"
    assert corpus_names["Payloads"] == ["payloads"], "Payloads mapping mismatch"
    print("  [PASS] 'Payloads' dynamically injected into MedRAG corpus_names.")

    db_dir = str(Path(__file__).resolve().parent / "MedRAG" / "corpus")
    print(f"\nInitializing MedRAG DocExtracter for corpus 'Payloads' in: {db_dir}...")
    doc_ext = DocExtracter(db_dir=db_dir, cache=True, corpus_name="Payloads")
    
    # Test extracting the sample document: PMC517508_01
    sample_id = "PMC517508_01"
    extracted = doc_ext.extract([sample_id])
    assert len(extracted) == 1, f"Expected 1 extracted doc, got {len(extracted)}"
    doc = extracted[0]
    
    print("\n  [PASS] Successfully extracted document using MedRAG DocExtracter:")
    print(f"    ID: {doc.get('id')}")
    print(f"    Title: {doc.get('title')}")
    print(f"    Content Excerpt: {doc.get('content')[:200]}...")

if __name__ == "__main__":
    test_payloads_native_integration()
