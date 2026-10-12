"""Unified facade for resume data extraction."""

from typing import Any, Dict
from extraction.contact_extractor import ContactExtractor
from extraction.database_tool_extractor import DatabaseToolExtractor
from extraction.education_extractor import EducationExtractor
from extraction.experience_extractor import ExperienceExtractor
from extraction.framework_extractor import FrameworkExtractor
from extraction.language_extractor import LanguageExtractor


class ResumeExtractor:
    """Facade class to orchestrate all specialized regex extractors."""

    @classmethod
    def extract_resume_data(cls, text: str) -> Dict[str, Any]:
        """Runs all extractors on the provided resume text.

        Returns a consolidated dictionary with all extracted categories.
        """
        if not text:
            return {
                "contacts": {},
                "languages": [],
                "frameworks": [],
                "databases_and_tools": [],
                "education": [],
                "experience": [],
            }

        return {
            "contacts": ContactExtractor.extract_contacts(text),
            "languages": LanguageExtractor.extract_languages(text),
            "frameworks": FrameworkExtractor.extract_frameworks(text),
            "databases_and_tools": DatabaseToolExtractor.extract_databases_and_tools(text),
            "education": EducationExtractor.extract_education(text),
            "experience": ExperienceExtractor.extract_experience(text),
        }