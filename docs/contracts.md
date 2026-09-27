# Data Contracts Specification: ResumeLens (IntegrativeTask_FAH)

---

## 1. Introduction

The **ResumeLens** system converts unstructured and semi-structured candidate resumes into verified qualification assessments using a mathematically grounded formal language pipeline:
1. **`extraction/`**: Lexical scanning and entity extraction via Regular Expressions (Regex / DFAs).
2. **`normalization/`**: Terminology standardization via Finite-State Transducers (FSTs).
3. **`automata/`**: Profile evaluation via Deterministic/Nondeterministic Finite Automata (DFAs/NFAs).
4. **`dsl/` & `visualization/`**: Profile specification using a `textX` Domain-Specific Language and graphical output generation.

To ensure independent development, team decoupling, and strict type safety across module boundaries, this document specifies the **Data Contracts** (Python dictionary / JSON schema interfaces) for data passed between pipeline stages within `IntegrativeTask_FAH`.

---

## 2. Contract 1: Extraction Module (`extraction/`) -> Normalization Module (`normalization/`)

### 2.1 Purpose
Passes extracted raw entities, contact metadata, and unnormalized candidate skills extracted from raw resume files (`samples/resumes/*.txt`) to the normalization engine.

### 2.2 Input Interface
* **Source:** Relative file path to a text resume inside `samples/resumes/`.
* **Data Type:** `str`

```
input_file_path: str = "samples/resumes/cv_fullstack.txt"
```

### 2.3 Output Data Contract (JSON / Python Dict)
```json
{
  "document_metadata": {
    "file_name": "cv_fullstack.txt",
    "file_path": "samples/resumes/cv_fullstack.txt",
    "encoding": "utf-8",
    "character_count": 1420
  },
  "candidate_info": {
    "extracted_email": "alex.dev@gmail.com",
    "extracted_phone": "+1-555-019-2834",
    "extracted_dates": ["2020-2022", "2022-2026"],
    "total_years_experience": 6
  },
  "raw_skills": [
    "js",
    "React.js",
    "NodeJS",
    "Postgres",
    "Git",
    "sklearn",
    "Python3"
  ]
}
```

---

## 3. Contract 2: Normalization Module (`normalization/`) -> Automata Module (`automata/`)

### 3.1 Purpose
Converts surface variation tokens (`js`, `React.js`, `sklearn`) into canonical, standardized tokens (`JAVASCRIPT`, `REACT`, `SCIKIT_LEARN`) and category tags using FST regular relations. Outputs an ordered token sequence ready for state-machine evaluation.

### 3.2 Input Interface
Consumes the dictionary output produced by Contract 1 (`extraction/`).

### 3.3 Output Data Contract (JSON / Python Dict)
```json
{
  "candidate_id": "alex.dev@gmail.com",
  "source_file": "cv_fullstack.txt",
  "years_experience": 6,
  "normalized_stream": [
    {
      "raw_token": "js",
      "canonical_token": "JAVASCRIPT",
      "category": "FRONTEND"
    },
    {
      "raw_token": "React.js",
      "canonical_token": "REACT",
      "category": "FRONTEND"
    },
    {
      "raw_token": "NodeJS",
      "canonical_token": "NODEJS",
      "category": "BACKEND"
    },
    {
      "raw_token": "Postgres",
      "canonical_token": "POSTGRESQL",
      "category": "DATABASE"
    },
    {
      "raw_token": "Git",
      "canonical_token": "GIT",
      "category": "TOOLS"
    },
    {
      "raw_token": "sklearn",
      "canonical_token": "SCIKIT_LEARN",
      "category": "MACHINE_LEARNING"
    }
  ],
  "ordered_canonical_tokens": [
    "JAVASCRIPT",
    "REACT",
    "NODEJS",
    "POSTGRESQL",
    "GIT",
    "SCIKIT_LEARN"
  ]
}
```

---

## 4. Contract 3: Automata Module (`automata/`) -> DSL Module (`dsl/`)

### 4.1 Purpose
Delivers the evaluation results from evaluating candidate token streams against DFA/NFA candidate profiles (e.g., `FullStackDeveloper`, `MLEngineer`). Includes state execution traces, boolean acceptance decisions, and missing requirements.

### 4.2 Input Interface
Consumes the canonical token list and candidate metadata produced by Contract 2 (`normalization/`).

### 4.3 Output Data Contract (JSON / Python Dict)
```json
{
  "candidate_id": "alex.dev@gmail.com",
  "evaluation_timestamp": "2026-09-27T11:20:00Z",
  "profiles_evaluated": {
    "FullStackDeveloper": {
      "accepted": true,
      "execution_path": [
        {"state": "q0", "consumed_symbol": "JAVASCRIPT", "next_state": "q1"},
        {"state": "q1", "consumed_symbol": "REACT", "next_state": "q2"},
        {"state": "q2", "consumed_symbol": "NODEJS", "next_state": "q3"},
        {"state": "q3", "consumed_symbol": "POSTGRESQL", "next_state": "q4_ACCEPT"}
      ],
      "missing_requirements": []
    },
    "MLEngineer": {
      "accepted": false,
      "execution_path": [
        {"state": "q0", "consumed_symbol": "JAVASCRIPT", "next_state": "q0_REJECT"}
      ],
      "failing_state": "q0_REJECT",
      "missing_requirements": ["PYTHON", "TENSORFLOW_OR_PYTORCH"]
    }
  }
}
```

---

## 5. Contract 4: DSL Module (`dsl/`) -> Visualization Module (`visualization/`)

### 5.1 Purpose
Combines candidate validation data from Contract 3 with parsed `textX` DSL profile definitions to generate graphical output artifacts (e.g., Graphviz DFA transition diagrams, HTML summary dashboards, or execution graphs).

### 5.2 Input Interface (textX Meta-Model & Validation Result)
* **DSL Definition File:** `dsl/profiles.tx`
* **Candidate Evaluation Object:** Contract 3 dictionary structure.

```text
// Sample textX Grammar excerpt (dsl/profiles.tx)
Profile:
    'Profile' name=ID '{'
        'min_experience:' min_exp=INT
        'required_skills:' skills+=ID['->']
    '}'
;
```

### 5.3 Output Data Contract & Output Artifacts
```json
{
  "report_summary": {
    "candidate": "alex.dev@gmail.com",
    "primary_match": "FullStackDeveloper",
    "match_status": "APPROVED",
    "generated_artifacts": [
      "visualization/output/alex_dev_dfa_trace.png",
      "visualization/output/alex_dev_report.html"
    ]
  }
}
```

#### Rendered Visual Artifacts:
1. **`visualization/output/<candidate>_dfa_trace.png`:** Graphviz visual rendering highlighting the active computation path through state transitions.
2. **`visualization/output/<candidate>_report.html`:** Interactive dashboard summarizing candidate metadata, raw term extraction, FST canonical mapping, and DFA match status per profile.