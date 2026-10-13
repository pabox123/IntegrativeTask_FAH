# ResumeLens — Stage 1: Data Extraction Design Document

## 1. Architecture Overview
The **Data Extraction** module (Stage 1 of the ResumeLens pipeline) is responsible for processing raw, unstructured text strings from candidate resumes and extracting structured professional tokens. The module is engineered using modular, object-oriented design principles with independent domain-specific extractors and a unified facade (`ResumeExtractor`) to orchestrate execution.

---
## 2. Component Specifications & Taxonomies

### 2.1. ContactExtractor
The `ContactExtractor` class identifies and extracts primary communication channels and professional profile links from resume text using standardized regular expressions.

* **Email Pattern (`EMAIL_REGEX`)**: Matches RFC-compliant email address structures.
  `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b`
* **Phone Pattern (`PHONE_REGEX`)**: Captures standard phone numbers, accommodating optional country codes, area codes, and standard delimiters (`-`, `.`, spaces).
  `\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b`
* **LinkedIn Pattern (`LINKEDIN_REGEX`)**: Identifies public LinkedIn profile URLs and handles.
  `\b(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+\/?\b`

**Methods:**
* `extract_contacts(text: str) -> Dict[str, Optional[str]]`: Returns the first matched email, phone, and LinkedIn handle.

---

### 2.2. LanguageExtractor
The `LanguageExtractor` isolates core programming languages using word boundaries (`\b`) and case-insensitive matching to prevent partial substring collisions.

* **Recognized Tokens (`LANGUAGES_REGEX`)**:
    * `Python` (supports optional versioning like `Python3`)
    * `Java`, `JavaScript` (`JS`), `TypeScript` (`TS`)
    * `C++`, `C#`
    * `Ruby`, `PHP`, `Swift`, `Kotlin`, `Go`, `Rust`
    * `SQL`, `R`

**Methods:**
* `extract_languages(text: str) -> List[str]`: Compiles patterns using `re.VERBOSE | re.IGNORECASE`, filters duplicates case-insensitively, and returns a normalized list of language tokens.

---

### 2.3. FrameworkExtractor
The `FrameworkExtractor` targets popular software engineering frameworks, libraries, and runtime environments across backend, frontend, and data science domains.

* **Recognized Tokens (`FRAMEWORKS_REGEX`)**:
    * Frontend: `React` (with optional `.js`), `Vue` (with optional `.js`), `Angular`
    * Backend & Runtimes: `Node` (with optional `.js`), `NodeJS`, `Express` (with optional `.js`), `Spring` (with optional `Boot`), `Django`, `Flask`, `FastAPI`
    * Data Science & ML: `Pandas`, `NumPy`, `Scikit-learn` / `sklearn`, `TensorFlow`, `PyTorch`

**Methods:**
* `extract_frameworks(text: str) -> List[str]`: Extracts, cleans, and deduplicates framework mentions.

---

### 2.4. DatabaseToolExtractor
The `DatabaseToolExtractor` handles relational/NoSQL databases, version control systems, containerization platforms, CI/CD tools, Infrastructure as Code (IaC), cloud providers, and operational tools.

* **Recognized Tokens (`DATABASES_TOOLS_REGEX`)**:
    * Databases: `PostgreSQL` / `Postgres`, `MySQL`, `MariaDB`, `MongoDB`, `Redis`, `SQLite`, `Oracle`, `DynamoDB`
    * Version Control & DevOps: `Git`, `GitHub`, `GitLab`, `Docker`, `Kubernetes` / `K8s`, `Jenkins`, `Terraform`, `Linux`, `Bash`
    * Cloud Providers: `AWS`, `GCP`, `Azure`
    * Utilities & Management: `Postman`, `Jira`

**Methods:**
* `extract_databases_and_tools(text: str) -> List[str]`: Compiles tool tokens using verbose regex compilation and returns a unique normalized list.

---

### 2.5. EducationExtractor
The `EducationExtractor` scans text for academic degrees and formal educational qualifications.

* **Recognized Tokens (`EDUCATION_REGEX`)**:
    * Degrees & Levels: `Bachelor` (with optional `'s` or field specifications), `Master` (with optional `'s` or field specifications), `Ph.D.`, `Doctorate`, `B.Sc.`, `M.Sc.`, `B.A.`, `M.A.`, `Undergraduate`, `Postgraduate`
    * Multilingual Degree Markers: `Ingeniería`, `Engineering`, `Grado`, `Licenciatura`

**Methods:**
* `extract_education(text: str) -> List[str]`: Returns unique academic qualifications identified in the resume text.

---

### 2.6. ExperienceExtractor
The `ExperienceExtractor` parses professional tenure indicators, capturing both cumulative years of experience and chronological date ranges.

* **Patterns (`YEARS_EXPERIENCE_REGEX` & `DATE_RANGES_REGEX`)**:
    * Tenure Statements: E.g., `5+ years of experience`, `over 3 years`.
    * Date Ranges: Captures month-year combinations (e.g., `Jan 2019 to Present`, `March 2020 – Current`) and four-digit year intervals (`2020 - 2023`).

**Methods:**
* `extract_experience(text: str) -> List[str]`: Combines tenure and temporal range patterns to compile a deduplicated list of experience tokens.

## 3. Unified Facade (`ResumeExtractor`)

The `ResumeExtractor` acts as the single entry point for Stage 1 execution, centralizing all domain extractors into a unified workflow.

```python
class ResumeExtractor:
    @classmethod
    def extract_resume_data(cls, text: str) -> Dict[str, Any]:
```
* **Execution Flow:**
  1. Validates input text; returns an empty schema structure if input is null or empty.
  2. Invokes individual domain extractors (`ContactExtractor`, `LanguageExtractor`, `FrameworkExtractor`, `DatabaseToolExtractor`, `EducationExtractor`, and `ExperienceExtractor`).
  3. Returns a consolidated dictionary containing all categorized extraction results, formatted for downstream consumption by Stage 2 (FST Normalization).