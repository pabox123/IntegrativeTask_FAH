# ResumeLens — Test Cases & Validation Scenarios Design

## 1. Overview & Testing Strategy
This document outlines the test strategy and validation scenarios for **ResumeLens**. The system evaluates candidate qualification sequences against four target professional profiles:
1. **Full Stack Developer** (Reference Profile 1)
2. **Machine Learning Engineer** (Reference Profile 2)
3. **DevOps Engineer** (Custom Software Engineering Profile)
4. **NLP Engineer** (Custom AI/Data Profile)

Testing is conducted at two levels:
* **Stage-by-Stage Verification:** Testing each pipeline stage independently (Regex Extraction, FST Normalization, Automata Classification, and DSL Parsing).
* **End-to-End Profile Evaluation:** Testing complete candidate résumés to verify expected acceptance or rejection outcomes.

---

## 2. Test Cases by Pipeline Stage

### Stage 1: Data Extraction (Regex)
* **Objective:** Ensure regex patterns extract raw qualification tokens, contact details, and dates without throwing errors or missing key terms.
* **TC-EXT-01 (Valid Extraction):** Input containing `"Skills: JS, React.js, NodeJS, Postgres, Git"` yields extracted tokens `["JS", "React.js", "NodeJS", "Postgres", "Git"]`.
* **TC-EXT-02 (Noise Handling):** Input containing unformatted text and filler words properly isolates candidate qualifications.

### Stage 2: Qualification Normalization & Sorting (FST)
* **Objective:** Verify Finite-State Transducers correctly translate variant strings into canonical tokens and place them in profile-specific canonical order.
* **TC-NORM-01 (Programming Languages):** `"JS"` / `"Javascript"` / `"js"` $\rightarrow$ `"JAVASCRIPT"`.
* **TC-NORM-02 (Frameworks & Libraries):** `"React.js"` / `"ReactJS"` $\rightarrow$ `"REACT"`; `"sklearn"` / `"scikit learn"` $\rightarrow$ `"SCIKIT_LEARN"`.
* **TC-NORM-03 (Databases & Tools):** `"Postgres"` / `"PostgreSQL"` $\rightarrow$ `"POSTGRESQL"`; `"k8s"` $\rightarrow$ `"KUBERNETES"`.
* **TC-NORM-04 (Canonical Sorting):** Input sequence `["Git", "NodeJS", "JS", "Postgres", "React.js"]` for Full Stack profile yields ordered sequence `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]`.

### Stage 3: Qualification Pattern Matching (Automata)
* **Objective:** Verify that DFAs/NFAs correctly transition to accepting states for valid qualification sequences and reject incomplete/out-of-order sequences.
* **TC-AUT-01 (DFA Evaluation):** Input `["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"]` $\rightarrow$ `ACCEPTED` for `MACHINE_LEARNING_ENGINEER`.
* **TC-AUT-02 (Incomplete Sequence):** Input `["PYTHON", "GIT"]` $\rightarrow$ `REJECTED` (missing data manipulation and ML library requirements).

### Stage 4: DSL Specification & Visualization (textX)
* **Objective:** Ensure the textX grammar validates candidate profile structure and rejects syntactically malformed specifications.
* **TC-DSL-01 (Valid DSL Parsing):** Correctly structured profile generates an HTML visual report.
* **TC-DSL-02 (Syntax Error Handling):** Missing mandatory candidate fields raises a DSL parse exception.

---

## 3. Profile-Specific Validation Scenarios

### 3.1. Profile 1: Full Stack Developer

| Case ID | Candidate Name | Input Qualification Tokens | Normalized & Ordered Canonical Sequence | Expected Status | Rationale |
|---|---|---|---|---|---|
| **FS-ACC-01** | Wednesday Addams | `JS, React.js, NodeJS, Postgres, Git` | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` | **ACCEPTED** | Satisfies Frontend, Backend, DB, and Version Control requirements. |
| **FS-ACC-02** | Alex Mercer | `TypeScript, Vue, Django, MySQL, REST API, Git` | `TYPESCRIPT, VUE, DJANGO, MYSQL, REST_API, GIT` | **ACCEPTED** | Valid alternative stack satisfying all profile layers. |
| **FS-REJ-01** | John Doe | `JS, HTML, CSS` | `JAVASCRIPT` | **REJECTED** | Lacks required Backend framework, Database, and Version Control. |
| **FS-REJ-02** | Jane Smith | `React.js, Postgres` | `REACT, POSTGRESQL` | **REJECTED** | Lacks primary programming language, backend framework, and Git. |

---

### 3.2. Profile 2: Machine Learning Engineer

| Case ID | Candidate Name | Input Qualification Tokens | Normalized & Ordered Canonical Sequence | Expected Status | Rationale |
|---|---|---|---|---|---|
| **ML-ACC-01** | Mary Jane Watson | `Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git` | `PYTHON, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, SQL, GIT` | **ACCEPTED** | Complete ML engineering stack covering data processing, ML, and DL. |
| **ML-ACC-02** | Bruce Banner | `Python, NumPy, PyTorch, SQL, Git` | `PYTHON, NUMPY, PYTORCH, SQL, GIT` | **ACCEPTED** | Valid deep learning-focused ML stack. |
| **ML-REJ-01** | Clark Kent | `Python, SQL, Git` | `PYTHON, SQL, GIT` | **REJECTED** | Missing required core ML framework (Scikit-learn/TensorFlow/PyTorch). |
| **ML-REJ-02** | Diana Prince | `R, Excel, Tableau` | `R, EXCEL, TABLEAU` | **REJECTED** | Lacks primary Python language and formal ML library requirements. |

---

### 3.3. Profile 3: DevOps Engineer (Custom Software Engineering Profile)

| Case ID | Candidate Name | Input Qualification Tokens | Normalized & Ordered Canonical Sequence | Expected Status | Rationale |
|---|---|---|---|---|---|
| **DO-ACC-01** | Tony Stark | `Linux, Bash, Docker, k8s, Jenkins, Terraform, AWS, Git` | `LINUX, BASH, DOCKER, KUBERNETES, JENKINS, TERRAFORM, AWS, GIT` | **ACCEPTED** | Complete DevOps stack (OS, Containerization, Orchestration, CI/CD, IaC, Cloud). |
| **DO-ACC-02** | Peter Parker | `Linux, Docker, Jenkins, AWS, Git` | `LINUX, DOCKER, JENKINS, AWS, GIT` | **ACCEPTED** | Satisfies core infrastructure, CI/CD, and deployment requirements. |
| **DO-REJ-01** | Barry Allen | `Bash, Git` | `BASH, GIT` | **REJECTED** | Lacks containerization (Docker) and CI/CD automation tools. |

---

### 3.4. Profile 4: NLP Engineer (Custom AI/Data Profile)

| Case ID | Candidate Name | Input Qualification Tokens | Normalized & Ordered Canonical Sequence | Expected Status | Rationale |
|---|---|---|---|---|---|
| **NLP-ACC-01** | Alan Turing | `Python, Tokenization, spaCy, BERT, Transformers, PyTorch, SQL` | `PYTHON, TOKENIZATION, SPACY, BERT, TRANSFORMERS, PYTORCH, SQL` | **ACCEPTED** | Complete NLP pipeline stack covering text preprocessing, models, and deep learning. |
| **NLP-ACC-02** | Grace Hopper | `Python, NLTK, HuggingFace, PyTorch, Git` | `PYTHON, NLTK, HUGGINGFACE, PYTORCH, GIT` | **ACCEPTED** | Valid NLP stack utilizing transformer hubs and classical NLP tools. |
| **NLP-REJ-01** | Arthur Pendelton | `Python, Pandas, Scikit-learn` | `PYTHON, PANDAS, SCIKIT_LEARN` | **REJECTED** | General ML candidate lacking specialized NLP libraries (spaCy/NLTK/Transformers). |

---

## 4. Edge Cases & Exception Handling

1. **Empty Skill Lists:**
    * *Scenario:* Résumé contains contact details but no extractable skills.
    * *Expected Outcome:* Stage 2 produces an empty list `[]`; Stage 3 automata evaluate to `REJECTED`.
2. **Unrecognized Skill Variants:**
    * *Scenario:* Résumé lists an obscure tool not defined in FST transitions (e.g., `"Cobol"`).
    * *Expected Outcome:* FST passes the unmapped token through or filters it gracefully without breaking execution.
3. **Out-of-Order Input Qualifications:**
    * *Scenario:* Candidate lists skills in arbitrary order (`Git, Postgres, React.js, JS`).
    * *Expected Outcome:* Stage 2 `canonical_order.py` reorders tokens into standard profile sequence before passing to Stage 3 DFA, ensuring order independence during evaluation.
