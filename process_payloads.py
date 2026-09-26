#!/usr/bin/env python3
"""
Process Clinical Payload Dataset for MedRAG.
Focuses strictly on textual data and completely ignores `img_path`.
Produces:
1. Structured text dataset: HealthCareAgent/data/text_payloads.jsonl
2. MedRAG corpus format: HealthCareAgent/MedRAG/corpus/payloads/chunk/payloads.jsonl
3. Sample output summary and statistics.
"""

import os
import glob
import json
import re
from pathlib import Path

def parse_clinical_text(raw_text: str):
    """Extract metadata and case presentation from raw clinical text block."""
    meta = {
        "title": "",
        "source": "",
        "demographics": "",
        "target_disease": "",
        "case_presentation": ""
    }
    
    title_match = re.search(r"Title:\s*(.+)", raw_text)
    if title_match:
        meta["title"] = title_match.group(1).strip()
        
    source_match = re.search(r"Source:\s*(.+)", raw_text)
    if source_match:
        meta["source"] = source_match.group(1).strip()
        
    demo_match = re.search(r"Patient Demographics:\s*(.+)", raw_text)
    if demo_match:
        meta["demographics"] = demo_match.group(1).strip()
        
    disease_match = re.search(r"Target Disease Indications:\s*(.+)", raw_text)
    if disease_match:
        meta["target_disease"] = disease_match.group(1).strip()
        
    pres_match = re.search(r"Case Presentation:\s*\n(.*)", raw_text, re.DOTALL)
    if pres_match:
        meta["case_presentation"] = pres_match.group(1).strip()
    else:
        # Fallback if no explicit "Case Presentation:" header
        meta["case_presentation"] = raw_text.strip()
        
    return meta

def process_single_payload(file_path: str):
    """
    Process one payload file.
    Focus on text only, ignore img_path.
    """
    case_id = Path(file_path).stem
    
    with open(file_path, "r", encoding="utf-8") as f:
        items = json.load(f)
        
    text_blocks = []
    image_captions = []
    image_footnotes = []
    
    for item in items:
        item_type = item.get("type")
        if item_type == "text":
            txt = item.get("text", "").strip()
            if txt:
                text_blocks.append(txt)
        elif item_type == "image":
            # Explicitly IGNORE item["img_path"] as instructed!
            caps = item.get("image_caption", [])
            notes = item.get("image_footnote", [])
            for c in caps:
                if c and isinstance(c, str):
                    image_captions.append(c.strip())
            for n in notes:
                if n and isinstance(n, str):
                    image_footnotes.append(n.strip())

    combined_case_text = "\n\n".join(text_blocks)
    meta = parse_clinical_text(combined_case_text)
    
    # Title resolution
    title = meta["title"] if meta["title"] else f"Case {case_id}"
    
    # Build clean textual content
    content_parts = []
    if meta["demographics"]:
        content_parts.append(f"Demographics: {meta['demographics']}")
    if meta["target_disease"]:
        content_parts.append(f"Target Disease: {meta['target_disease']}")
    if meta["case_presentation"]:
        content_parts.append(f"Case Presentation: {meta['case_presentation']}")
    else:
        content_parts.append(combined_case_text)
        
    if image_captions:
        content_parts.append("Image Observations: " + " | ".join(image_captions))
    if image_footnotes:
        content_parts.append("Image Annotations: " + " | ".join(image_footnotes))
        
    full_content = "\n\n".join(content_parts)
    
    # Normalize whitespaces for retrieval
    normalized_content = re.sub(r"\s+", " ", full_content).strip()
    
    # Document record
    doc_record = {
        "id": case_id,
        "title": title,
        "source": meta["source"],
        "demographics": meta["demographics"],
        "target_disease": meta["target_disease"],
        "content": normalized_content,
        "raw_text": combined_case_text,
        "image_captions": image_captions,
        "image_footnotes": image_footnotes
    }
    
    # MedRAG corpus standard format:
    # Requires id, title, content, contents
    medrag_snippet = {
        "id": case_id,
        "title": title,
        "content": normalized_content,
        "contents": f"{title}. {normalized_content}"
    }
    
    return doc_record, medrag_snippet

def main():
    base_dir = Path(__file__).resolve().parent
    payloads_dir = base_dir / "payload_for_ref" / "payloads"
    
    out_data_dir = base_dir / "data"
    out_data_dir.mkdir(parents=True, exist_ok=True)
    
    medrag_chunk_dir = base_dir / "MedRAG" / "corpus" / "payloads" / "chunk"
    medrag_chunk_dir.mkdir(parents=True, exist_ok=True)
    
    files = sorted(glob.glob(str(payloads_dir / "*.json")))
    print(f"Total payload JSON files found: {len(files)}")
    
    all_docs = []
    medrag_lines = []
    
    sample_file = payloads_dir / "PMC517508_01.json"
    if sample_file.exists():
        sample_doc, sample_snippet = process_single_payload(str(sample_file))
        print("\n" + "=" * 60)
        print("SAMPLE ACCESS & TEXT EXTRACTION: PMC517508_01.json")
        print("=" * 60)
        print(f"ID: {sample_doc['id']}")
        print(f"Title: {sample_doc['title']}")
        print(f"Demographics: {sample_doc['demographics']}")
        print(f"Target Disease: {sample_doc['target_disease']}")
        print(f"Image captions extracted (ignoring img_path): {sample_doc['image_captions']}")
        print(f"Image footnotes extracted (ignoring img_path): {sample_doc['image_footnotes']}")
        print(f"Content preview (first 250 chars):\n  {sample_doc['content'][:250]}...")
        print("=" * 60 + "\n")
        
    for fpath in files:
        doc, snippet = process_single_payload(fpath)
        all_docs.append(doc)
        medrag_lines.append(json.dumps(snippet, ensure_ascii=False))
        
    # 1. Save general text-only dataset
    out_text_jsonl = out_data_dir / "text_payloads.jsonl"
    with open(out_text_jsonl, "w", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print(f"Saved {len(all_docs)} processed text documents to: {out_text_jsonl}")
    
    # 2. Save MedRAG chunk format
    medrag_jsonl = medrag_chunk_dir / "payloads.jsonl"
    with open(medrag_jsonl, "w", encoding="utf-8") as f:
        f.write("\n".join(medrag_lines) + "\n")
    print(f"Saved MedRAG chunk corpus to: {medrag_jsonl}")
    
    # Statistics summary
    total_words = sum(len(d["content"].split()) for d in all_docs)
    avg_words = total_words / len(all_docs) if all_docs else 0
    diseases = set(d["target_disease"] for d in all_docs if d["target_disease"])
    
    summary = {
        "total_documents": len(all_docs),
        "total_words": total_words,
        "avg_words_per_case": round(avg_words, 1),
        "unique_target_diseases_count": len(diseases),
        "sample_diseases": list(diseases)[:10]
    }
    
    with open(out_data_dir / "dataset_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print("\nDataset Processing Complete!")
    print(f"Summary: {json.dumps(summary, indent=2)}")

if __name__ == "__main__":
    main()
