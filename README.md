# ResumeLens

ResumeLens is an automated resume-screening tool based on formal languages and automata theory. It receives a plain-text resume, extracts relevant information, normalizes skills, compares the candidate's profile against finite automata, and generates a DSL specification together with an HTML report.

## Features

- Data extraction using regular expressions:
  - Name, email, and location.
  - Programming languages.
  - Frameworks and libraries.
  - Databases and tools.
  - Experience and education.
- Skill-name and alias normalization using finite-state transducers (FSTs).
- Classification using automata for four professional profiles:
  - Full Stack Developer.
  - Machine Learning Engineer.
  - DevOps Engineer.
  - NLP Engineer.
- Structural validation of each profile using a `textX`-based DSL grammar.
- Generation of three output files for each resume:
  - An HTML visual report.
  - A DSL-validated `.resume` specification.
  - A JSON summary.
- Individual processing, processing of all sample resumes, and an interactive console interface.

## Requirements

- Python 3.10 or later.
- `pip`.
- Windows, Linux, or macOS.

Project dependencies are declared in [`requirements.txt`](requirements.txt):

- `pyformlang`: finite automata and transducers.
- `textX`: DSL grammar and validation.
- `pytest`: unit and integration testing.

## Installation

From the repository root, create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows CMD

```bat
python -m venv venv
venv\Scripts\activate.bat
```

### Linux or macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

Run all commands from the repository root.

### Process a resume

```bash
python resumeLens/main.py samples/resumes/cv_fullstack.txt
```

You can also process any text file containing a resume:

```bash
python resumeLens/main.py path/to/my_resume.txt
```

The program displays the five stages of the pipeline:

1. Extraction using regular expressions.
2. Normalization using finite-state transducers.
3. Classification using automata.
4. DSL specification validation.
5. HTML report generation.

### Process all samples

```bash
python resumeLens/main.py --demo
```

The included samples are located in `samples/resumes/` and represent the four supported profiles.

### Use the interactive interface

```bash
python ui/cli.py
```

The interface allows you to:

1. Load a resume from a path.
2. Choose one of the sample resumes.
3. Process all sample resumes.
4. Open the last generated HTML report.
0. Exit.

## Generated output

Files are automatically saved in `output/`. For an input file named `cv_fullstack.txt`, the following files are generated:

```text
output/
├── cv_fullstack_profile.html    # Visual report to open in a browser
├── cv_fullstack_profile.resume  # Profile validated by the DSL
└── cv_fullstack_result.json     # Name, email, skills, and classification
```

The JSON output has a structure similar to:

```json
{
  "name": "Candidate Name",
  "email": "candidate@example.com",
  "skills": [
    "JAVASCRIPT",
    "REACT",
    "NODE_JS",
    "POSTGRESQL",
    "GIT"
  ],
  "classification": {
    "profile": "Full Stack Developer",
    "result": "ACCEPTED"
  }
}
```

If the resume does not match any profile, the result is:

```json
{
  "classification": {
    "profile": "Unknown",
    "result": "REJECTED"
  }
}
```

## Recommended input format

The system processes UTF-8 plain-text files. For the best results, organize the resume with clear labels and sections. For example:

```text
Candidate Name
Email: candidate@example.com
Phone: +57 300 000 0000
Location: Bogotá, Colombia

PROFESSIONAL EXPERIENCE
Full Stack Developer
Company · 3 years
- Developed web applications using React and NodeJS.

EDUCATION
Bachelor of Systems Engineering

TECHNICAL SKILLS
Programming Languages: JavaScript, TypeScript, Python
Frameworks: React.js, NodeJS
Databases: PostgreSQL, MongoDB
Tools: Git, Docker
```

The extractor recognizes common skill-name variants. For example, `JS`, `JavaScript`, and `Javascript` are converted to `JAVASCRIPT`; `NodeJS` and `Node.js` are converted to `NODE_JS`; and `Postgres` is converted to `POSTGRESQL`.

## Architecture

The processing pipeline follows this flow:

```text
Plain-text resume
        │
        ▼
extraction/        Regex: data extraction
        │
        ▼
normalization/     FST: canonical and ordered skills
        │
        ▼
automata/          DFA: profile classification
        │
        ▼
dsl/               textX: CandidateProfile validation
        │
        ▼
visualization/     HTML: visual report
```

### Main components

| Directory | Responsibility |
|---|---|
| `extraction/` | Extracts contacts, skills, experience, and education using regular expressions. |
| `normalization/` | Converts aliases and variants into canonical skills using FSTs. |
| `automata/` | Defines the DFA validators for the four supported profiles. |
| `dsl/` | Parses and validates the structured candidate profile using `textX`. |
| `visualization/` | Generates the HTML report. |
| `resumeLens/` | Contains the main pipeline orchestration. |
| `ui/` | Provides the interactive console interface. |
| `tests/` | Contains unit, integration, and end-to-end tests. |
| `samples/` | Contains sample resumes and expected outputs. |
| `docs/` | Contains design, formalization, data-contract, and academic documentation. |
| `output/` | Stores generated files. |

## Supported profiles

Profiles and their validators are defined in `automata/`:

| Profile | File |
|---|---|
| Full Stack Developer | `automata/full_stack_dfa.py` |
| Machine Learning Engineer | `automata/ml_engineer_dfa.py` |
| DevOps Engineer | `automata/devops_dfa.py` |
| NLP Engineer | `automata/nlp_engineer_dfa.py` |

Classification returns the first accepted profile in the order configured in `resumeLens/main.py`. A resume is rejected when its normalized skills do not form a sequence accepted by any of the automata.

## Running the tests

With the virtual environment active, run:

```bash
python -m pytest -q
```

For detailed output:

```bash
python -m pytest -v
```

The test suite covers:

- Information extraction.
- Skill normalization.
- Automata validation.
- DSL parsing and validation.
- Integration between pipeline stages.
- Classification of all four sample resumes.
- Rejection of unqualified candidates.

## Repository structure

```text
IntegrativeTask_FAH/
├── automata/
├── docs/
├── dsl/
├── extraction/
├── normalization/
├── output/
├── resumeLens/
├── samples/
├── tests/
├── ui/
├── visualization/
├── requirements.txt
└── README.md
```

## Team

- **Krystal Giraldo** — information extraction.
- **Valeria Piza** — skill normalization.
- **Miguel Pabón** — automata, DSL, and integration.

## Academic information

- **Course:** Discrete Computation and Structures III.
- **Term:** 2026-2.
- **Project:** Integrative Task 1.

For the formalization and design decisions, see the documents available in [`docs/`](docs/).
