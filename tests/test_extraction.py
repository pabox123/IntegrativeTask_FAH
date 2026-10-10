import pytest
from extraction.contact_extractor import ContactExtractor
from extraction.language_extractor import LanguageExtractor
from extraction.framework_extractor import FrameworkExtractor
from extraction.database_tool_extractor import DatabaseToolExtractor
from extraction.education_extractor import EducationExtractor
from extraction.experience_extractor import ExperienceExtractor
from extraction.resume_extractor import ResumeExtractor


def test_contact_extractor():
    #Test extraction of emails, phones, and LinkedIn profiles
    text = "Reach me at test.user@gmail.com, phone: 123-456-7890, or linkedin.com/in/testuser."
    result = ContactExtractor.extract_contacts(text)

    assert result["extracted_email"] == "test.user@gmail.com"
    assert result["extracted_phone"] == "123-456-7890"
    assert result["extracted_linkedin"] == "linkedin.com/in/testuser"


def test_tc_ext_01_valid_extraction():
    #TC-EXT-01: Valid extraction of mixed tokens (JS, React.js, NodeJS, Postgres, Git)
    text = "Skills: JS, React.js, NodeJS, Postgres, Git"
    data = ResumeExtractor.extract_resume_data(text)

    assert "JS" in data["languages"]
    assert "React.js" in data["frameworks"]
    assert "NodeJS" in data["frameworks"] or "NodeJS" in data["languages"] # depends on category classification
    assert "Postgres" in data["databases_and_tools"]
    assert "Git" in data["databases_and_tools"] or "Git" in data["frameworks"]


def test_tc_ext_02_noise_handling():
    #TC-EXT-02: Noise handling and isolation of candidate qualifications from unformatted text
    noisy_text = "Hello team, my name is John and you can check that my core tech stack includes Python and Docker, without extra filler words."
    data = ResumeExtractor.extract_resume_data(noisy_text)

    assert "Python" in data["languages"]
    assert "Docker" in data["databases_and_tools"]
    assert len(data["education"]) == 0
    assert len(data["experience"]) == 0


def test_resume_extractor_facade():
    #Test the unified facade with a complete resume text
    resume_text = (
        "Jane Doe - Software Engineer. "
        "Contact: jane.doe@techcorp.com, phone: 123-456-7890, linkedin.com/in/janedoe. "
        "Skills: Python, React, PostgreSQL. "
        "Holds a Bachelor degree. "
        "5 years of experience, working from Jan 2019 to Present."
    )

    data = ResumeExtractor.extract_resume_data(resume_text)

    assert data["contacts"]["extracted_email"] == "jane.doe@techcorp.com"
    assert data["contacts"]["extracted_phone"] == "123-456-7890"
    assert data["contacts"]["extracted_linkedin"] == "linkedin.com/in/janedoe"
    assert "Python" in data["languages"]
    assert "React" in data["frameworks"]
    assert "PostgreSQL" in data["databases_and_tools"]
    assert "Bachelor" in data["education"]
    assert "5 years of experience" in data["experience"]


def test_resume_extractor_empty():
    #Test facade behavior with empty or null input
    data = ResumeExtractor.extract_resume_data("")

    assert data["contacts"] == {}
    assert data["languages"] == []
    assert data["frameworks"] == []
    assert data["databases_and_tools"] == []
    assert data["education"] == []
    assert data["experience"] == []

def test_edge_case_casing_extremes():
       #Test resilience against all-lowercase and all-uppercase resume formatting.
    lowercase_text = "python, react, postgresql, bachelor degree, 3 years of experience."
    data_lower = ResumeExtractor.extract_resume_data(lowercase_text)

    assert "python" in [l.lower() for l in data_lower["languages"]]
    assert "react" in [f.lower() for f in data_lower["frameworks"]]
    assert "postgresql" in [d.lower() for d in data_lower["databases_and_tools"]]

    uppercase_text = "PYTHON, REACT, POSTGRESQL, BACHELOR"
    data_upper = ResumeExtractor.extract_resume_data(uppercase_text)

    assert len(data_upper["languages"]) > 0
    assert len(data_upper["frameworks"]) > 0


def test_edge_case_multiline_bullet_points():
    """Test extraction from typical bulleted and multiline resume layouts."""
    multiline_resume = """
    Jane Developer
    Email: jane.dev@company.org | Phone: 987-654-3210
    
    SKILLS & STACK:
    * Languages: Python, Java
    * Frameworks: Django, Spring Boot
    * Databases: MySQL, Redis
    
    EDUCATION:
    - Master of Science in Computer Science
    
    EXPERIENCE:
    - Worked for 4+ years in software engineering.
    """

    data = ResumeExtractor.extract_resume_data(multiline_resume)

    assert data["contacts"]["extracted_email"] == "jane.dev@company.org"
    assert data["contacts"]["extracted_phone"] == "987-654-3210"
    assert "Python" in data["languages"]
    assert "Java" in data["languages"]
    assert "Django" in data["frameworks"]
    assert "Spring Boot" in data["frameworks"]
    assert "MySQL" in data["databases_and_tools"]
    assert "Redis" in data["databases_and_tools"]
    assert len(data["education"]) > 0
    assert len(data["experience"]) > 0


def test_edge_case_partial_contacts():
    """Test behavior when contact info is partially missing (e.g., only email present)."""
    text = "Only my email is here: contact@domain.com. No phone or linkedin."
    data = ResumeExtractor.extract_resume_data(text)

    assert data["contacts"]["extracted_email"] == "contact@domain.com"
    assert data["contacts"]["extracted_phone"] is None
    assert data["contacts"]["extracted_linkedin"] is None
