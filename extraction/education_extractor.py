import re
from typing import List

class EducationExtractor:
    #VERBOSE = None
    #  bachelor and master: captures academic degree with its field of study if available
    EDUCATION_REGEX = r"""
        \b(?:
            Bachelor(?:'s)?(?:\s+of\s+\w+)? | 
            Master(?:'s)?(?:\s+of\s+\w+)? |
            Ph\.?D\.? |
            Doctorate |
            B\.?Sc\.? |
            M\.?Sc\.? |
            B\.?A\.? |
            M\.?A\.? |
            Undergraduate |
            Postgraduate |
            Ingenier[íi]a |
            Engineering |
            Grado |
            Licenciatura
        )\b
    """

    @classmethod
    def extract_education(cls, text: str) -> List[str]:
        # compile pattern
        pattern = re.compile(cls.EDUCATION_REGEX, re.VERBOSE | re.IGNORECASE)
        # search all matches
        matches = pattern.findall(text)
        # normalize
        found_education = []
        seen = set()
        for edu in matches:
            # clean spaces
            clean_edu = edu.strip()
            # case-insensitive, no duplicate values
            upper_edu = clean_edu.upper()
            if upper_edu not in seen:
                seen.add(upper_edu)
                found_education.append(clean_edu)

        return found_education