import html
import json
import os
import re
import sys
from typing import Any, Dict, List

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from automata.devops_dfa import validate_devops_profile
from automata.full_stack_dfa import validate_full_stack_profile
from automata.ml_engineer_dfa import validate_ml_engineer_profile
from automata.nlp_engineer_dfa import validate_nlp_engineer_profile
from dsl.parser import ResumeParser
from dsl.validator import ProfileValidator
from extraction.resume_extractor import ResumeExtractor
from normalization.canonical import SkillNormalizerPipeline
from visualization.html_generator import generate_html_report as generate_html_visualization

OUTPUT_DIR: str = os.path.join(ROOT_DIR, "output")
SAMPLES: List[str] = [
    os.path.join(ROOT_DIR, "samples", "resumes", "cv_fullstack.txt"),
    os.path.join(ROOT_DIR, "samples", "resumes", "cv_ml.txt"),
    os.path.join(ROOT_DIR, "samples", "resumes", "cv_devops.txt"),
    os.path.join(ROOT_DIR, "samples", "resumes", "cv_nlp.txt"),
]

PROFILE_VALIDATORS: Dict[str, Any] = {
    "Full Stack Developer": validate_full_stack_profile,
    "Machine Learning Engineer": validate_ml_engineer_profile,
    "DevOps Engineer": validate_devops_profile,
    "NLP Engineer": validate_nlp_engineer_profile,
}

PROFILE_REQUIREMENTS: Dict[str, List[str]] = {
    "Full Stack Developer": (
        "JAVASCRIPT TYPESCRIPT REACT ANGULAR VUE NODE_JS DJANGO "
        "SPRING_BOOT EXPRESS POSTGRESQL MYSQL MONGODB SQL NOSQL GIT"
    ).split(),
    "Machine Learning Engineer": (
        "PYTHON R PANDAS NUMPY SCIKIT_LEARN XGBOOST TENSORFLOW PYTORCH "
        "SQL POSTGRESQL MYSQL BIGQUERY GIT"
    ).split(),
    "DevOps Engineer": (
        "PYTHON BASH POWERSHELL DOCKER KUBERNETES HELM JENKINS GITLAB_CI "
        "GITHUB_ACTIONS TERRAFORM ANSIBLE CLOUDFORMATION AWS AZURE GCP "
        "PROMETHEUS GRAFANA ELK GIT"
    ).split(),
    "NLP Engineer": (
        "PYTHON SQL BASH SPACY NLTK GENSIM PYTORCH TENSORFLOW TRANSFORMERS "
        "BERT ROBERTA POSTGRESQL MYSQL ELASTICSEARCH DOCKER GIT JUPYTER FASTAPI"
    ).split(),
}

EXTRA_SKILL_ALIASES: Dict[str, str] = {
    "nodejs": "NODE_JS",
    "node.js": "NODE_JS",
    "rest api": "REST_API",
    "rest apis": "REST_API",
    "scikit learn": "SCIKIT_LEARN",
    "scikit-learn": "SCIKIT_LEARN",
    "tensor flow": "TENSORFLOW",
    "py torch": "PYTORCH",
    "xgboost": "XGBOOST",
    "github actions": "GITHUB_ACTIONS",
    "gitlab ci": "GITLAB_CI",
    "cloudformation": "CLOUDFORMATION",
    "prometheus": "PROMETHEUS",
    "grafana": "GRAFANA",
    "elk stack": "ELK",
    "helm": "HELM",
    "ansible": "ANSIBLE",
    "powershell": "POWERSHELL",
    "jupyter": "JUPYTER",
    "fastapi": "FASTAPI",
    "bert": "BERT",
    "roberta": "ROBERTA",
    "gensim": "GENSIM",
    "elasticsearch": "ELASTICSEARCH",
}


def banner(title: str) -> None:
    print(f"\n=== {title} ===")


def _candidate_name(text: str) -> str:
    first_line: str = next((line.strip() for line in text.splitlines() if line.strip()), "")
    return first_line if first_line and "@" not in first_line else "Unknown"


def _candidate_location(text: str) -> str:
    match = re.search(r"(?im)^Location:\s*(.+)$", text)
    return match.group(1).strip() if match else "Unknown"


def extract(text: str) -> Dict[str, Any]:
    banner("1. Extraction (regex)")
    data: Dict[str, Any] = ResumeExtractor.extract_resume_data(text)
    data["name"] = _candidate_name(text)
    data["email"] = data.get("contacts", {}).get("extracted_email")
    data["location"] = _candidate_location(text)

    raw_skills: List[str] = []
    for key in ("languages", "frameworks", "databases_and_tools"):
        raw_skills.extend(data.get(key, []))

    lowered_text: str = text.lower()
    for term, canonical in EXTRA_SKILL_ALIASES.items():
        if term in lowered_text:
            raw_skills.append(canonical)
    data["skills"] = raw_skills

    print(f"name: {data['name']}")
    print(f"email: {data['email']}")
    print(f"skills: {len(data['skills'])}")
    print(f"experience entries: {len(data.get('experience', []))}")
    print(f"education entries: {len(data.get('education', []))}")
    return data


def normalize(extracted: Dict[str, Any]) -> List[str]:
    banner("2. Normalization (FST)")
    raw: List[str] = extracted.get("skills", [])
    skills: List[str] = SkillNormalizerPipeline().normalize_and_sort_skills(raw)
    print(f"raw: {raw}")
    print(f"normalized: {skills}")
    return skills


def _ordered_profile_skills(skills: List[str], profile: str) -> List[str]:
    available = set(skills)
    return [skill for skill in PROFILE_REQUIREMENTS[profile] if skill in available]


def classify(skills: List[str]) -> Dict[str, str]:
    banner("3. Classification (automata)")
    accepted: Any = None
    for profile, validator in PROFILE_VALIDATORS.items():
        sequence: List[str] = _ordered_profile_skills(skills, profile)
        result: bool = bool(sequence) and validator(sequence)
        status: str = "ACCEPTED" if result else "REJECTED"
        print(f"{profile}: {status}")
        if result and accepted is None:
            accepted = profile

    if accepted:
        return {"profile": accepted, "result": "ACCEPTED"}
    return {"profile": "Unknown", "result": "REJECTED"}


def _quote(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _duration(value: Any) -> str:
    match = re.search(r"\d+(?:\.\d+)?\s+(?:years?|months?)", str(value), re.IGNORECASE)
    return match.group(0) if match else "1 year"


def build_spec(extracted: Dict[str, Any], skills: List[str], classification: Dict[str, str]) -> str:
    banner("4. Specification (textX)")
    lines: List[str] = [
        "CandidateProfile {",
        f"    name: {_quote(extracted.get('name', 'Unknown'))}",
        f"    email: {_quote(extracted.get('email') or 'unknown@example.com')}",
        f"    location: {_quote(extracted.get('location', 'Unknown'))}",
        f"    current_role: {_quote(classification['profile'])}",
        '    summary: "Candidate profile generated by ResumeLens"',
    ]

    for experience in extracted.get("experience", [])[:3]:
        lines.extend([
            "    Experience {",
            '        company: "Extracted resume experience"',
            f"        duration: {_quote(_duration(experience))}",
            '        description: "Professional experience"',
            "    }",
        ])
    for skill in skills:
        lines.append(f"    Skill: {skill}")

    description: str = (
        f"The normalized qualifications satisfy an accepted "
        f"{classification['profile']} pattern."
        if classification["result"] == "ACCEPTED"
        else "The normalized qualifications do not satisfy any accepted profile pattern."
    )
    lines.extend([
        "    Evaluation {",
        f"        profile: {_quote(classification['profile'])}",
        f"        result: {classification['result']}",
        f"        description: {_quote(description)}",
        "    }",
        "}",
    ])
    spec: str = "\n".join(lines)

    candidate = ResumeParser().parse_string(spec)
    validation = ProfileValidator().validate(candidate)
    print("validation passed" if validation.is_valid else
          f"validation failed:\n{validation.summary()}")
    return spec


def generate_html_report(extracted: Dict[str, Any], skills: List[str], classification: Dict[str, str]) -> str:
    return generate_html_visualization(extracted, skills, classification)


def visualize(extracted: Dict[str, Any], skills: List[str], classification: Dict[str, str]) -> str:
    banner("5. Visualization (HTML)")
    report: str = generate_html_report(extracted, skills, classification)
    print(f"report size: {len(report)} bytes")
    return report


def process_resume_text(text: str) -> Dict[str, Any]:
    extracted = extract(text)
    skills = normalize(extracted)
    classification = classify(skills)
    spec = build_spec(extracted, skills, classification)
    report = visualize(extracted, skills, classification)
    return {
        "extracted": extracted,
        "skills": skills,
        "classification": classification,
        "evaluation": classification,
        "dsl": spec,
        "html": report,
    }


def process_resume(file_path: str) -> Dict[str, Any]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    print(f"\nProcessing {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        result = process_resume_text(file.read())

    name: str = os.path.splitext(os.path.basename(file_path))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    paths: Dict[str, str] = {
        "html": os.path.join(OUTPUT_DIR, f"{name}_profile.html"),
        "dsl": os.path.join(OUTPUT_DIR, f"{name}_profile.resume"),
        "json": os.path.join(OUTPUT_DIR, f"{name}_result.json"),
    }
    with open(paths["html"], "w", encoding="utf-8") as file:
        file.write(result["html"])
    with open(paths["dsl"], "w", encoding="utf-8") as file:
        file.write(result["dsl"])
    with open(paths["json"], "w", encoding="utf-8") as file:
        json.dump({
            "name": result["extracted"].get("name"),
            "email": result["extracted"].get("email"),
            "skills": result["skills"],
            "classification": result["classification"],
        }, file, indent=2)

    print("\nSaved:")
    for path in paths.values():
        print(f"  {path}")
    result["paths"] = paths
    return result


def run_demo() -> None:
    results = [
        process_resume(sample) for sample in SAMPLES if os.path.exists(sample)
    ]
    banner("Summary")
    for result in results:
        classification = result["classification"]
        print(
            f"{result['extracted'].get('name', 'Unknown'):25s} "
            f"{classification['profile']:30s} {classification['result']}"
        )


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python resumeLens/main.py <resume.txt> | --demo")
        return
    if sys.argv[1] == "--demo":
        run_demo()
    else:
        process_resume(sys.argv[1])


if __name__ == "__main__":
    main()