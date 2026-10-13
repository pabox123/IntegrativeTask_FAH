from typing import List, Dict
from normalization.fst_normalizer import (
    build_programming_languages_fst,
    build_frameworks_fst,
    build_databases_fst,
    build_aiml_fst,
    build_devops_fst,
    normalize_token
)

# Canonical Category Hierarchy and Target Profile Sequences
CATEGORY_HIERARCHY = [
    "PROGRAMMING_LANGUAGES",
    "FRONTEND_FRAMEWORKS",
    "BACKEND_FRAMEWORKS",
    "DATABASES",
    "DEVOPS_TOOLS",
    "AI_ML_TOOLS"
]

# Canonical skill rank map for deterministic sorting
CANONICAL_RANK = {
    # Programming Languages
    "JAVASCRIPT": 10, "TYPESCRIPT": 11, "PYTHON": 12, "JAVA": 13, "CPP": 14,
    # Front
    "REACT": 20, "VUE": 21, "ANGULAR": 22,
    # Back
    "NODE_JS": 30, "EXPRESS": 31, "DJANGO": 32, "SPRING_BOOT": 33, "REST_API": 34,
    # Databases
    "POSTGRESQL": 40, "MYSQL": 41, "MARIADB": 42, "MONGODB": 43, "REDIS": 44, "SQLITE": 45, "SQL": 46,
    # DevOps and Infrastructure
    "LINUX": 50, "BASH": 51, "GIT": 52, "DOCKER": 53, "KUBERNETES": 54, "JENKINS": 55, "TERRAFORM": 56, "AWS": 57, "GCP": 58, "AZURE": 59,
    # AI / ML and Data Science
    "PANDAS": 60, "NUMPY": 61, "SCIKIT_LEARN": 62, "TENSORFLOW": 63, "PYTORCH": 64, "SPACY": 65, "NLTK": 66, "BERT": 67, "TRANSFORMERS": 68
}


class SkillNormalizerPipeline:
    """
    Unified normalization pipeline that orchestrates Category FSTs and applies canonical ordering.
    """
    def __init__(self):
        self.fst_pl = build_programming_languages_fst()
        self.fst_fw = build_frameworks_fst()
        self.fst_db = build_databases_fst()
        self.fst_ai = build_aiml_fst()
        self.fst_do = build_devops_fst()

    def normalize_single_token(self, token: str) -> str:
        """
        Passes a token through all category FSTs until a canonical mapping is found.
        """
        for fst in [self.fst_pl, self.fst_fw, self.fst_db, self.fst_ai, self.fst_do]:
            normalized = normalize_token(token, fst)
            if normalized != token.upper() or normalized in CANONICAL_RANK:
                return normalized
        return token.upper()

    def normalize_and_sort_skills(self, raw_tokens: List[str]) -> List[str]:
        """
        Translates raw extracted skill tokens to canonical form and eliminates order dependency.
        """
        canonical_set = set()
        for token in raw_tokens:
            norm = self.normalize_single_token(token)
            canonical_set.add(norm)

        # Sort tokens based on canonical rank hierarchy
        sorted_canonical = sorted(
            list(canonical_set),
            key=lambda skill: CANONICAL_RANK.get(skill, 999)
        )
        return sorted_canonical


def canonicalize_extracted_data(extracted_dict: Dict[str, List[str]]) -> List[str]:
    """
    Main entry point interfacing Stage 1 (Extraction) output with Stage 2 (Normalization).
    Accepts extracted category dictionary and returns a single canonical ordered skill list.
    """
    pipeline = SkillNormalizerPipeline()
    all_raw_tokens = []

    for category, tokens in extracted_dict.items():
        if isinstance(tokens, list):
            all_raw_tokens.extend(tokens)

    return pipeline.normalize_and_sort_skills(all_raw_tokens)


if __name__ == "__main__":
    # Local verification test with out-of-order raw skills
    raw_extracted_resume = {
        "programming_languages": ["JS", "py"],
        "frameworks": ["React.js", "NodeJS"],
        "databases": ["Postgres"],
        "tools": ["Git", "Docker"]
    }

    pipeline = SkillNormalizerPipeline()
    raw_list = ["Git", "NodeJS", "JS", "Postgres", "React.js", "py", "Docker"]

    print("--- ResumeLens: Canonical Ordering Verification ---")
    print(f"Raw Input Skills (Out of order): {raw_list}")

    canonical_output = pipeline.normalize_and_sort_skills(raw_list)
    print(f"\nCanonical Ordered Output: {canonical_output}")
