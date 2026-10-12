import io
import os
import sys
from typing import Any, Dict, List

import pytest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TESTS_DIR: str = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR: str = os.path.dirname(TESTS_DIR)
RESUMELENS_DIR: str = os.path.join(ROOT_DIR, "resumeLens")

for path in [ROOT_DIR, RESUMELENS_DIR]:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

try:
    from main import process_resume, process_resume_text
except ModuleNotFoundError:
    from resumeLens.main import process_resume, process_resume_text

from extraction.resume_extractor import ResumeExtractor
from normalization.canonical import SkillNormalizerPipeline, canonicalize_extracted_data
from automata.full_stack_dfa import validate_full_stack_profile
from automata.ml_engineer_dfa import validate_ml_engineer_profile
from automata.devops_dfa import validate_devops_profile
from automata.nlp_engineer_dfa import validate_nlp_engineer_profile


class TestStageToStageIntegration:

    def test_extraction_to_normalization_flow(self) -> None:
        resume_snippet = (
            "Alex Morgan\n"
            "Email: alex.morgan@testdomain.com\n"
            "Technical Skills: JavaScript, React.js, NodeJS, Postgres, Git\n"
            "Experience: 4 years of experience as Full Stack Engineer\n"
            "Education: Bachelor of Science in Software Engineering\n"
        )
        extracted: Dict[str, Any] = ResumeExtractor.extract_resume_data(resume_snippet)
        assert extracted is not None
        assert extracted["contacts"]["extracted_email"] == "alex.morgan@testdomain.com"
        assert "JavaScript" in extracted["languages"]
        assert "React.js" in extracted["frameworks"]
        assert "Postgres" in extracted["databases_and_tools"]

        pipeline = SkillNormalizerPipeline()
        raw_skills: List[str] = []
        for key in ("languages", "frameworks", "databases_and_tools"):
            raw_skills.extend(extracted.get(key, []))

        normalized_skills: List[str] = pipeline.normalize_and_sort_skills(raw_skills)
        expected_skills: List[str] = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        assert normalized_skills == expected_skills

    def test_normalization_to_automata_classification(self) -> None:
        pipeline = SkillNormalizerPipeline()
        raw_fullstack = ["NodeJS", "Git", "JS", "Postgres", "React.js"]
        normalized = pipeline.normalize_and_sort_skills(raw_fullstack)
        assert normalized == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        assert validate_full_stack_profile(normalized) is True

    def test_canonicalize_extracted_data_interface(self) -> None:
        extracted_mock = {
            "languages": ["Python", "SQL"],
            "frameworks": ["Pandas", "sklearn"],
            "databases_and_tools": ["Docker", "Git"],
        }
        normalized: List[str] = canonicalize_extracted_data(extracted_mock)
        assert "PYTHON" in normalized
        assert "SCIKIT_LEARN" in normalized
        assert "GIT" in normalized


class TestEndToEndPipeline:

    SAMPLE_RESUMES: Dict[str, str] = {
        "cv_fullstack.txt": "Full Stack Developer",
        "cv_ml.txt": "Machine Learning Engineer",
        "cv_devops.txt": "DevOps Engineer",
        "cv_nlp.txt": "NLP Engineer",
    }

    @pytest.mark.parametrize("filename,expected_profile", SAMPLE_RESUMES.items())
    def test_pipeline_classifies_sample_resumes_correctly(self, filename: str, expected_profile: str) -> None:
        sample_path: str = os.path.join(ROOT_DIR, "samples", "resumes", filename)
        if not os.path.exists(sample_path):
            sample_path = os.path.join(RESUMELENS_DIR, "samples", "resumes", filename)

        assert os.path.exists(sample_path), f"Sample file not found: {sample_path}"

        result: Dict[str, Any] = process_resume(sample_path)

        assert "extracted" in result
        assert "skills" in result
        assert "classification" in result
        assert "dsl" in result
        assert "html" in result
        assert "paths" in result

        assert result["classification"]["profile"] == expected_profile
        assert result["classification"]["result"] == "ACCEPTED"

        assert len(result["skills"]) > 0
        assert len(result["dsl"]) > 0
        assert "CandidateProfile" in result["dsl"]
        assert len(result["html"]) > 0
        assert "<html" in result["html"].lower()

        paths: Dict[str, str] = result["paths"]
        assert os.path.exists(paths["html"])
        assert os.path.exists(paths["dsl"])
        assert os.path.exists(paths["json"])

    def test_pipeline_rejects_unqualified_candidate(self) -> None:
        unqualified_cv = (
            "Juan Perez\n"
            "Email: juan@correo.com\n"
            "Location: Bogota, Colombia\n"
            "Skills: cooking, gardening, photography\n"
            "Experience: Chef for 5 years\n"
            "Education: High School Diploma\n"
        )
        result: Dict[str, Any] = process_resume_text(unqualified_cv)
        assert result["classification"]["result"] == "REJECTED"
        assert result["classification"]["profile"] == "Unknown"
        assert len(result["dsl"]) > 0
        assert len(result["html"]) > 0

    def test_pipeline_orchestration_consistency(self) -> None:
        sample_path: str = os.path.join(ROOT_DIR, "samples", "resumes", "cv_fullstack.txt")
        assert os.path.exists(sample_path)

        with open(sample_path, "r", encoding="utf-8") as f:
            cv_text = f.read()

        file_result = process_resume(sample_path)
        text_result = process_resume_text(cv_text)

        assert file_result["classification"] == text_result["classification"]
        assert file_result["skills"] == text_result["skills"]
        assert file_result["extracted"]["email"] == text_result["extracted"]["email"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])