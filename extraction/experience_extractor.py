import re
from typing import List


class ExperienceExtractor:

    #regex patterns for experience years
    YEARS_EXPERIENCE_REGEX = r"""
        \b(?:
            \d{1,2}\+?\s*(?:years?|yrs?)(?:\s+of\s+experience)? |
            (?:over|more\s+than)\s+\d{1,2}\s+(?:years?|yrs?)
        )\b
    """
    #regex patterns for date ranges
    DATE_RANGES_REGEX = r"""
        \b(?:
            (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{4}
            \s*(?:-|to|–)\s*
            (?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{4}|Present|Current|Now)
            |
            \d{4}\s*(?:-|to|–)\s*(?:\d{4}|Present|Current|Now)
        )\b
    """

    @classmethod
    def extract_experience(cls, text: str) -> List[str]:
        found_experience = []
        seen = set()

        #combine regex patterns
        patterns = [cls.YEARS_EXPERIENCE_REGEX, cls.DATE_RANGES_REGEX]

        for p_str in patterns:
            pattern = re.compile(p_str, re.VERBOSE | re.IGNORECASE)
            matches = pattern.findall(text)

            for item in matches:
                clean_item = item.strip()
                upper_item = clean_item.upper()
                if upper_item not in seen:
                    seen.add(upper_item)
                    found_experience.append(clean_item)

        return found_experience