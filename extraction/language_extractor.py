import re
from typing import List


class LanguageExtractor:
    # regex pattern with word boundaries for common frameworks and libraries
    LANGUAGES_REGEX = r"""
        \b(?:
            Python[3]? |
            Java |
            JavaScript |
            JS |
            TypeScript |
            TS |
            C\+\+ |
            C\# |
            Ruby |
            PHP |
            Swift |
            Kotlin |
            Go |
            Rust |
            SQL |
            R
        )\b
    """

    @classmethod
    def extract_languages(cls, text: str) -> List[str]:
        #compile pattern
        pattern = re.compile(cls.LANGUAGES_REGEX, re.VERBOSE | re.IGNORECASE)

        # search all matches
        matches = pattern.findall(text)

        # normalize
        found_languages = []
        seen = set()
        for lang in matches:
            # clean spaces
            clean_lang = lang.strip()
            # case-insensitive, no duplicate values
            upper_lang = clean_lang.upper()
            if upper_lang not in seen:
                seen.add(upper_lang)
                found_languages.append(clean_lang)

        return found_languages