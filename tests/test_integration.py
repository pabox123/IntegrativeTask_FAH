

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestEndToEndPipeline:

    SAMPLE_RESUMES = {
        "cv_fullstack.txt": "Full Stack Developer",
        "cv_ml.txt": "Machine Learning Engineer",
        "cv_devops.txt": "DevOps Engineer",
        "cv_nlp.txt": "NLP Engineer",
    }

    @pytest.mark.parametrize("filename,expected_profile", SAMPLE_RESUMES.items())
    def test_pipeline_classifies_correctly(self, filename, expected_profile):
        try:
            from main import process_resume
        except ImportError:
            pytest.skip("main.py not yet available")

        path = os.path.join('samples', 'resumes', filename)
        if not os.path.exists(path):
            pytest.skip(f"Sample file {filename} not found")

        result = process_resume(path)
        assert result["evaluation"]["profile"] == expected_profile
        assert result["evaluation"]["result"] == "ACCEPTED"

    def test_pipeline_rejects_invalid_candidate(self):
        try:
            from main import process_resume_text
        except ImportError:
            pytest.skip("main.py not yet available")

        text = """
        Juan Perez
        Email: juan@correo.com
        Skills: knitting, cooking, gardening
        """
        result = process_resume_text(text)
        assert result["evaluation"]["result"] == "REJECTED"


class TestPipelineComponents:

    def test_extraction_returns_dict(self):
        try:
            from extraction.extractor import extract_resume_data
        except ImportError:
            pytest.skip("extraction module not yet available")

        text = "Santiago Restrepo. Email: santiago@correo.com. Skills: Python, Git."
        data = extract_resume_data(text)
        assert isinstance(data, dict)
        assert "skills" in data

    def test_normalization_returns_canonical_list(self):
        try:
            from normalization.fst_normalizer import normalize_skills
        except ImportError:
            pytest.skip("normalization module not yet available")

        raw = ["js", "React.js", "nodejs", "postgres"]
        normalized = normalize_skills(raw)
        assert all(isinstance(s, str) for s in normalized)
        assert all(s == s.upper() for s in normalized)

    def test_automata_accepts_canonical_skills(self):
        try:
            from automata.full_stack_dfa import FullStackDFA
        except ImportError:
            pytest.skip("automata module not yet available")

        dfa = FullStackDFA()
        result = dfa.validate(["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])
        assert result["result"] == "ACCEPTED"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])