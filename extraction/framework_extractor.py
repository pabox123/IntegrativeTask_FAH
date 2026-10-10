import re
from typing import List


class FrameworkExtractor:
    # regex pattern with word boundaries for common frameworks and libraries
    FRAMEWORKS_REGEX = r"""
        \b(?:
            React(?:\.js)? |
            Vue(?:\.js)? |
            Angular |
            Node(?:\.js)? |
            NodeJS |
            Express(?:\.js)? |
            Spring(?:\s+Boot)? |
            Django |
            Flask |
            FastAPI |
            Pandas |
            NumPy |
            Scikit-learn |
            sklearn |
            TensorFlow |
            PyTorch
        )\b
    """

    @classmethod
    def extract_frameworks(cls, text: str) -> List[str]:
        # compile pattern
        pattern = re.compile(cls.FRAMEWORKS_REGEX, re.VERBOSE | re.IGNORECASE)

        # search all matches
        matches = pattern.findall(text)

        # normalize
        found_frameworks = []
        seen = set()
        for fw in matches:
            # clean spaces
            clean_fw = fw.strip()
            # case-insensitive, no duplicate values
            upper_fw = clean_fw.upper()
            if upper_fw not in seen:
                seen.add(upper_fw)
                found_frameworks.append(clean_fw)

        return found_frameworks