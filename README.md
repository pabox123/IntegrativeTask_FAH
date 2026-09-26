# ResumeLens: Formal Language-Based Resume Screening

## Team Members
- **Krystal Giraldo**
- **Valeria Piza**
- **Miguel Pabon**

## Project Overview
ResumeLens processes textual résumés and determines whether candidates satisfy qualification patterns for professional profiles using formal language models:
- Regular expressions for information extraction
- Finite-state transducers for qualification normalization
- Finite automata for pattern recognition
- Context-free grammars (textX) for structured validation

## Supported Profiles
1. Full Stack Developer (predefined)
2. Machine Learning Engineer (predefined)
3. DevOps Engineer (team-defined, Software Engineering)
4. NLP Engineer (team-defined, AI/Data)

## Project Structureresumelens/
````
├── extraction/ # Regex-based information extraction (Krystal)
├── normalization/ # FST-based qualification normalization (Valeria)
├── automata/ # DFA/NFA for profile recognition (Miguel)
├── dsl/ # textX grammar for candidate profiles (Miguel)
├── ui/ # User interface
├── visualization/ # HTML/Markdown report generation
├── tests/ # Unit and integration tests
├── docs/ # Design documents and literature review
└── samples/ # Sample résumés and expected outputs
````
## Installationbash
Create virtual environment
````
python -m venv venv
````
Activate virtual environment
Windows:
````
venv\Scripts\activate
````
Linux/Mac:
````
source venv/bin/activate
````
Install dependencies
````
pip install -r requirements.txt
````
## Usage
```bash
python main.py --resume samples/resumes/resume_wednesday_addams.txtCourse Information
Course: Computación y Estructuras Discretas III
Term: 2026-2
Deadline: October 11, 2026
