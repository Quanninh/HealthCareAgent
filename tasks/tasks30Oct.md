# Weekly Task Board — Clinical SLM (RAG + Finetuning)

> **How to use:** Tick a box only when the atomic task is *done*. Sub-bullets = acceptance criteria / notes.

---

## 👤 Khoa — Disease Labeling Expansion

**Goal:** Expand beyond the 15 low-case diseases to build a stronger finetuning dataset.

**New disease list to label:**
- Tuberculosis
- Melioidosis
- Amoebiasis
- Neurocysticercosis
- Echinococcosis
- Schistosomiasis
- Leprosy
- Leishmaniasis
- Cryptococcosis
- Histoplasmosis
- Paragonimiasis
- Lymphatic Filariasis
- Malaria
- Covid19
- Dengue

**Tasks:**
- [ ] Union the new disease list with the current list → expect ~20+ diseases total
- [ ] Run the labeling framework (LLM approach) on the expanded list
- [ ] Evaluate the quality of the labeling output
- [ ] Convert labeled data into SOAP format (structured case text)
- [ ] *(Optional)* Discuss user query + system prompt with the team

---

## 👤 Khoi — RAG

**Tasks:**
- [ ] Read the newest IBM paper — https://arxiv.org/pdf/2609.03874v1 *(target: Saturday)*
- [ ] Report on difficulty of implementing IBM's approach
  - [ ] Assess code setup effort
  - [ ] Assess running time
- [ ] Decide models (generation, judge, embedding) with Anh Minh
- [ ] Decide user query + system prompt with Anh Minh (and other members, e.g., Khoa)

---

## 👤 Anh Minh — RAG

**Tasks:**
- [ ] Understand how to put the SOAP format into naiveRAG
- [ ] Run the evaluation process with a model **with NO RAG** to establish the benchmark
- [ ] Decide models (generation, judge, embedding) with Khoi
- [ ] Decide user query + system prompt with Khoi (and other members, e.g., Khoa)

---

## 👤 Ku Bo — Distillation & Finetune Evaluation

**Tasks:**
- [ ] Read 1 paper about distillation (read more if still unclear)
- [ ] Revise code to apply SFT or offline distillation process
- [ ] Revise the evaluation code for finetune
- [ ] Run the evaluation code for the base model to establish the baseline
  - Test set: ~20 cases from Khai's GT reasoning (18 POSITIVE + 2 OUT_OF_SCOPE)

---

## 👤 Khai — Reasoning Labeling

**Tasks:**
- [ ] Read MedCaseReasoning — https://arxiv.org/pdf/2505.11733
- [ ] Refine the reasoning GT so it conforms to a recognized format
- [ ] Decide on evaluation metrics for GT reasoning
- [ ] Write the evaluation code for the GT reasoning
- [ ] Run the evaluation code and report its quality

---

## 🔗 Cross-Team Sync Points (dependencies)

- [ ] **Khoi ↔ Anh Minh:** models (generation, judge, embedding)
- [ ] **Khoi ↔ Anh Minh ↔ Khoa:** user query + system prompt
- [ ] **Khoa → Anh Minh:** SOAP format feeds into naiveRAG
- [ ] **Khai → Ku Bo:** GT reasoning test set (18 POS + 2 OOS) feeds baseline eval