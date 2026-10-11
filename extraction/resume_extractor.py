from typing import Dict, Any
from extraction.contact_extractor import ContactExtractor
from extraction.language_extractor import LanguageExtractor
from extraction.framework_extractor import FrameworkExtractor
from extraction.database_tool_extractor import DatabaseToolExtractor
from extraction.education_extractor import EducationExtractor
from extraction.experience_extractor import ExperienceExtractor


class ResumeExtractor:
    @classmethod
    def extract_resume_data(cls, text: str) -> Dict[str, Any]:

        #runs all extractors on the provided resume
        if not text:
            return {
                "contacts": {},
                "languages": [],
                "frameworks": [],
                "databases_and_tools": [],
                "education": [],
                "experience": []
            }

        #returns a consolidated dictionary with all extracted categories
        return {
            "contacts": ContactExtractor.extract_contacts(text),
            "languages": LanguageExtractor.extract_languages(text),
            "frameworks": FrameworkExtractor.extract_frameworks(text),
            "databases_and_tools": DatabaseToolExtractor.extract_databases_and_tools(text),
            "education": EducationExtractor.extract_education(text),
            "experience": ExperienceExtractor.extract_experience(text)
        }
