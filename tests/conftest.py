
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dsl.parser import ResumeParser
from dsl.validator import ProfileValidator

def build_candidate_text(
        name="Test User",
        email="test@example.com",
        location="Bogota, Colombia",
        skills=None,
        profile="Full Stack Developer",
        result="ACCEPTED",
        description="Valid profile",
        experiences=None,
):
    """buidl a DSL string for a candidate profile"""
    if skills is None:
        skills = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]

    skills_block = "\n".join(f"        Skill: {s}" for s in skills)

    exp_block = ""
    if experiences:
        for exp in experiences:
            exp_block += f"""
        Experience {{
            company: "{exp['company']}"
            duration: "{exp['duration']}"
            description: "{exp['description']}"
        }}
"""

    return f"""
    CandidateProfile {{
        name: "{name}"
        email: "{email}"
        location: "{location}"
{exp_block}
{skills_block}

        Evaluation {{
            profile: "{profile}"
            result: {result}
            description: "{description}"
        }}
    }}
    """

@pytest.fixture
def build_text():
    """Return the DSL text builder helper (see ``build_candidate_text``)."""
    return build_candidate_text


@pytest.fixture
def parser():
    return ResumeParser()


@pytest.fixture
def validator():
    return ProfileValidator()


@pytest.fixture
def full_stack_skills():
    """ skills for a full stack developer"""
    return ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]


@pytest.fixture
def ml_skills():
    """ skills for a machine learning engineer."""
    return ["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"]


@pytest.fixture
def devops_skills():
    """canonical skill sequence accepted by the DevOps DFA"""
    return ["PYTHON", "DOCKER", "JENKINS", "TERRAFORM", "AWS", "PROMETHEUS", "GIT"]


@pytest.fixture
def nlp_skills():
    """canonical skill sequence accepted by the NLP DFA"""
    return ["PYTHON", "SPACY", "TRANSFORMERS", "BERT", "POSTGRESQL", "GIT"]


@pytest.fixture
def mixed_skills():
    """skills that dont fit any single profile cleanly"""
    return ["PYTHON", "REACT", "DOCKER", "GIT"]