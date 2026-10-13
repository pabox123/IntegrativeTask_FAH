
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from automata.full_stack_dfa import (
    get_full_stack_profile_info,
    validate_full_stack_profile,
)
from automata.ml_engineer_dfa import (
    get_ml_engineer_profile_info,
    validate_ml_engineer_profile,
)
from automata.devops_dfa import (
    get_devops_profile_info,
    validate_devops_profile,
)
from automata.nlp_engineer_dfa import (
    get_nlp_engineer_profile_info,
    validate_nlp_engineer_profile,
)


ALL_PROFILES = {
    "Full Stack Developer": validate_full_stack_profile,
    "Machine Learning Engineer": validate_ml_engineer_profile,
    "DevOps Engineer": validate_devops_profile,
    "NLP Engineer": validate_nlp_engineer_profile,
}


class TestFullStackDFA:

    def test_accepts_canonical_full_stack(self):
        skills = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        assert validate_full_stack_profile(skills)

    def test_accepts_with_typescript(self):
        skills = ["TYPESCRIPT", "ANGULAR", "DJANGO", "MYSQL", "GIT"]
        assert validate_full_stack_profile(skills)

    def test_accepts_with_vue(self):
        skills = ["JAVASCRIPT", "VUE", "SPRING_BOOT", "MONGODB", "GIT"]
        assert validate_full_stack_profile(skills)

    def test_accepts_extra_skills_after_accepting_state(self):
        skills = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT", "VUE"]
        assert validate_full_stack_profile(skills)

    def test_rejects_missing_frontend(self):
        skills = ["NODE_JS", "POSTGRESQL", "GIT"]
        assert not validate_full_stack_profile(skills)

    def test_rejects_missing_backend(self):
        skills = ["JAVASCRIPT", "REACT", "GIT"]
        assert not validate_full_stack_profile(skills)

    def test_rejects_missing_database(self):
        skills = ["JAVASCRIPT", "REACT", "NODE_JS", "GIT"]
        assert not validate_full_stack_profile(skills)

    def test_rejects_missing_version_control(self):
        skills = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL"]
        assert not validate_full_stack_profile(skills)

    def test_rejects_out_of_order_sequence(self):
        skills = ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT"]
        assert not validate_full_stack_profile(skills)

    def test_rejects_empty_skills(self):
        assert not validate_full_stack_profile([])

    def test_rejects_unrelated_skills(self):
        skills = ["PYTHON", "PANDAS", "TENSORFLOW"]
        assert not validate_full_stack_profile(skills)

    def test_rejects_only_git(self):
        assert not validate_full_stack_profile(["GIT"])


class TestMLEngineerDFA:

    def test_accepts_canonical_ml(self):
        skills = ["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"]
        assert validate_ml_engineer_profile(skills)

    def test_accepts_with_pytorch(self):
        skills = ["PYTHON", "NUMPY", "SCIKIT_LEARN", "PYTORCH", "SQL", "GIT"]
        assert validate_ml_engineer_profile(skills)

    def test_accepts_with_numpy_and_r(self):
        skills = ["R", "NUMPY", "XGBOOST", "PYTORCH", "POSTGRESQL", "GIT"]
        assert validate_ml_engineer_profile(skills)

    def test_rejects_missing_programming_language(self):
        skills = ["PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"]
        assert not validate_ml_engineer_profile(skills)

    def test_rejects_missing_ml_library(self):
        skills = ["PYTHON", "PANDAS", "SQL", "GIT"]
        assert not validate_ml_engineer_profile(skills)

    def test_rejects_missing_version_control(self):
        skills = ["PYTHON", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL"]
        assert not validate_ml_engineer_profile(skills)

    def test_rejects_web_skills_only(self):
        skills = ["JAVASCRIPT", "REACT", "NODE_JS"]
        assert not validate_ml_engineer_profile(skills)

    def test_rejects_empty(self):
        assert not validate_ml_engineer_profile([])


class TestDevOpsDFA:

    def test_accepts_canonical_devops(self, devops_skills):
        assert validate_devops_profile(devops_skills)

    def test_accepts_with_gitlab_ci(self):
        skills = ["BASH", "DOCKER", "GITLAB_CI", "ANSIBLE", "AZURE", "GRAFANA", "GIT"]
        assert validate_devops_profile(skills)

    def test_accepts_with_azure_and_gcp(self):
        skills = ["PYTHON", "KUBERNETES", "GITHUB_ACTIONS", "CLOUDFORMATION", "AZURE", "ELK", "GIT"]
        assert validate_devops_profile(skills)

    def test_rejects_missing_programming_language(self):
        skills = ["DOCKER", "JENKINS", "TERRAFORM", "AWS", "PROMETHEUS", "GIT"]
        assert not validate_devops_profile(skills)

    def test_rejects_missing_containers(self):
        skills = ["PYTHON", "JENKINS", "TERRAFORM", "AWS", "PROMETHEUS", "GIT"]
        assert not validate_devops_profile(skills)

    def test_rejects_missing_cloud(self):
        skills = ["PYTHON", "DOCKER", "JENKINS", "TERRAFORM", "PROMETHEUS", "GIT"]
        assert not validate_devops_profile(skills)

    def test_rejects_missing_version_control(self):
        skills = ["PYTHON", "DOCKER", "JENKINS", "TERRAFORM", "AWS", "PROMETHEUS"]
        assert not validate_devops_profile(skills)

    def test_rejects_web_skills(self):
        skills = ["JAVASCRIPT", "REACT", "POSTGRESQL"]
        assert not validate_devops_profile(skills)

    def test_rejects_empty(self):
        assert not validate_devops_profile([])


class TestNLPEngineerDFA:

    def test_accepts_canonical_nlp(self, nlp_skills):
        assert validate_nlp_engineer_profile(nlp_skills)

    def test_accepts_with_nltk_and_roberta(self):
        skills = ["SQL", "NLTK", "TRANSFORMERS", "ROBERTA", "ELASTICSEARCH", "DOCKER"]
        assert validate_nlp_engineer_profile(skills)

    def test_accepts_with_tensorflow(self):
        skills = ["PYTHON", "SPACY", "TENSORFLOW", "BERT", "MYSQL", "JUPYTER"]
        assert validate_nlp_engineer_profile(skills)

    def test_rejects_missing_programming_language(self):
        skills = ["SPACY", "NLTK", "TRANSFORMERS", "BERT", "POSTGRESQL", "GIT"]
        assert not validate_nlp_engineer_profile(skills)

    def test_rejects_missing_nlp_library(self):
        skills = ["PYTHON", "PYTORCH", "BERT", "POSTGRESQL", "GIT"]
        assert not validate_nlp_engineer_profile(skills)

    def test_rejects_missing_pretrained_model(self):
        skills = ["PYTHON", "SPACY", "PYTORCH", "POSTGRESQL", "GIT"]
        assert not validate_nlp_engineer_profile(skills)

    def test_rejects_ml_only_skills(self):
        skills = ["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW"]
        assert not validate_nlp_engineer_profile(skills)

    def test_rejects_empty(self):
        assert not validate_nlp_engineer_profile([])


class TestCrossProfile:

    @pytest.fixture
    def skills_by_profile(self, full_stack_skills, ml_skills, devops_skills, nlp_skills, mixed_skills):
        return {
            "Full Stack Developer": full_stack_skills,
            "Machine Learning Engineer": ml_skills,
            "DevOps Engineer": devops_skills,
            "NLP Engineer": nlp_skills,
            "mixed": mixed_skills,
        }

    @pytest.mark.parametrize("profile", list(ALL_PROFILES))
    def test_profile_skills_accepted_by_own_automaton(self, profile, skills_by_profile):
        validate = ALL_PROFILES[profile]
        assert validate(skills_by_profile[profile]), \
            f"{profile} should accept its own canonical skills"

    @pytest.mark.parametrize("accepted_profile", list(ALL_PROFILES))
    def test_other_profiles_reject_these_skills(self, accepted_profile, skills_by_profile):
        skills = skills_by_profile[accepted_profile]
        for profile, validate in ALL_PROFILES.items():
            if profile == accepted_profile:
                continue
            assert not validate(skills), \
                f"{profile} should reject {accepted_profile} skills"

    @pytest.mark.parametrize("profile", list(ALL_PROFILES))
    def test_mixed_skills_rejected_by_all(self, profile, skills_by_profile):
        assert not ALL_PROFILES[profile](skills_by_profile["mixed"]), \
            f"{profile} should reject mixed skills"


class TestProfileInfo:

    @pytest.mark.parametrize("info_fn", [
        get_full_stack_profile_info,
        get_ml_engineer_profile_info,
        get_devops_profile_info,
        get_nlp_engineer_profile_info,
    ])
    def test_profile_info_exposes_requirements(self, info_fn):
        info = info_fn()
        assert set(info) >= {"profile_name", "description", "canonical_order", "requirements", "pattern"}
        assert set(info["requirements"]) == set(info["canonical_order"])

    def test_profile_names_match_expected(self):
        assert get_full_stack_profile_info()["profile_name"] == "Full Stack Developer"
        assert get_ml_engineer_profile_info()["profile_name"] == "Machine Learning Engineer"
        assert get_devops_profile_info()["profile_name"] == "DevOps Engineer"
        assert get_nlp_engineer_profile_info()["profile_name"] == "NLP Engineer"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
