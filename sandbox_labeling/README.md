# Clinical Agent Sandbox Environment

> **Purpose:** Isolated execution environment and workspace for the 15 specialized Clinical Annotation Agents and Master Coordinator.

---

## 1. Directory Layout

```text
sandbox_labeling/
├── .agents/                               # Sandboxed Agent Customizations
│   └── skills/                            # 15 specialized disease agent skills + clinical-annotator
├── protocols/                             # Self-Contained Medical Reference Protocols
│   ├── 01_clinical_claim_ontology.md      # Ontology definition
│   ├── 02_clinical_claim_schema.md        # Claim schema specification
│   ├── 03_evidence_specificity_matrix.md  # Disease evidence criteria (E1/E2/E3)
│   └── 04_gold_standard_annotation_protocol.md # 12-step annotation protocol
├── workspace/                             # Agent Workspace (Inputs, Outputs, Logs, Prompts)
│   ├── labeled_pool/                      # 7,043 Adjudicated Candidate Pairs
│   │   ├── input/                         # 15 input JSONL files (one per target disease)
│   │   ├── output/                        # 15 output JSONL files produced by agents
│   │   ├── prompts/                       # Self-contained LLM prompts
│   │   ├── logs/                          # Agent run logs
│   │   └── coordinator_manifest.json      # Status and record counts
│   └── tier3_pool/                        # 10,388 Narrative Candidate Pairs
│       ├── input/                         # 15 input JSONL files
│       ├── output/                        # 15 output JSONL files
│       ├── prompts/                       # Self-contained LLM prompts
│       ├── logs/                          # Execution logs
│       └── coordinator_manifest.json
│
├── build_prompts.py                       # Prompt generation engine using OOP ClinicalPromptBuilder
└── build_disease_skills.py                # Skills compiler for sandbox/.agents/skills/
```

---

## 2. Agent Execution Workflow

All agents operate strictly within `sandbox/workspace/`:
1. **Inputs:** Loaded from `sandbox/workspace/{pool}/input/input_{disease_slug}.jsonl`
2. **Prompts:** Read from `sandbox/workspace/{pool}/prompts/prompt_{disease_slug}.md`
3. **Outputs:** Written to `sandbox/workspace/{pool}/output/output_{disease_slug}.jsonl`
4. **Logs:** Written to `sandbox/workspace/{pool}/logs/agent_{disease_slug}.log`

### Compiling Skills & Prompts

```bash
# 1. Compile 15 disease skills from medical matrix:
python3 sandbox/build_disease_skills.py

# 2. Generate prompt markdown files for target pool:
python3 sandbox/build_prompts.py --pool labeled_pool
python3 sandbox/build_prompts.py --pool tier3_pool
```
