
import re
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

VALID_PROFILES = [
    "Full Stack Developer",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "NLP Engineer",
]

VALID_RESULTS = ["ACCEPTED", "REJECTED"]

CANONICAL_SKILL_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]*$')

EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

DURATION_PATTERN = re.compile(
    r'^\d+(\.\d+)?\s+(years?|months?)$', re.IGNORECASE
)


def _skill_text(skill) -> str:
    """Return the textual token of a skill, whether it is a plain string
    or a parsed ``SkillEntry`` object produced by the textX grammar."""
    value = getattr(skill, 'value', skill)
    return str(value).strip()


class ViolationLevel(Enum):
    LEXICAL = "LEXICAL"
    STRUCTURAL = "STRUCTURAL"
    SEMANTIC = "SEMANTIC"


@dataclass
class Violation:
    level: ViolationLevel
    field_name: str
    message: str
    value: Optional[str] = None

    def __str__(self):
        prefix = f"[{self.level.value}]"
        if self.value is not None:
            return f"{prefix} {self.field_name}: {self.message} (got: '{self.value}')"
        return f"{prefix} {self.field_name}: {self.message}"


@dataclass
class ValidationResult:
    is_valid: bool = True
    violations: List[Violation] = field(default_factory=list)
    candidate_name: str = "Unknown"

    def add_violation(self, violation: Violation):
        self.violations.append(violation)
        self.is_valid = False

    def summary(self) -> str:
        lines = [
            f"Validation Report for: {self.candidate_name}",
            "=" * 55,
            f"Result: {'PASSED' if self.is_valid else 'REJECTED'}",
            f"Total violations: {len(self.violations)}",
            ]
        if self.violations:
            lines.append("")
            lines.append("Violations:")
            for i, v in enumerate(self.violations, 1):
                lines.append(f"  {i}. {v}")
        return "\n".join(lines)

class ProfileValidator:

    def __init__(self, valid_profiles=None):
        self.valid_profiles = valid_profiles or VALID_PROFILES


    def validate(self, candidate) -> ValidationResult:
        result = ValidationResult()
        result.candidate_name = getattr(candidate, 'name', 'Unknown')

        self._check_structural(candidate, result)
        self._check_lexical(candidate, result)
        self._check_semantic(candidate, result)

        return result

    def validate_or_raise(self, candidate) -> ValidationResult:
        result = self.validate(candidate)
        if not result.is_valid:
            raise ProfileRejectionError(result)
        return result

    def _check_structural(self, candidate, result: ValidationResult):
        name = getattr(candidate, 'name', None)
        if not name or not name.strip():
            result.add_violation(Violation(
                level=ViolationLevel.STRUCTURAL,
                field_name="name",
                message="Candidate name is required and cannot be empty",
                value=name,
            ))

        email = getattr(candidate, 'email', None)
        if not email or not email.strip():
            result.add_violation(Violation(
                level=ViolationLevel.STRUCTURAL,
                field_name="email",
                message="Email address is required",
                value=email,
            ))
        skills = getattr(candidate, 'skills', [])
        if not skills or len(skills) == 0:
            result.add_violation(Violation(
                level=ViolationLevel.STRUCTURAL,
                field_name="skills",
                message="At least one technical skill is required",
            ))

        evaluation = getattr(candidate, 'evaluation', None)
        if evaluation is None:
            result.add_violation(Violation(
                level=ViolationLevel.STRUCTURAL,
                field_name="evaluation",
                message="Qualification evaluation block is required",
            ))
        else:
            profile = getattr(evaluation, 'profile', None)
            if not profile or not profile.strip():
                result.add_violation(Violation(
                    level=ViolationLevel.STRUCTURAL,
                    field_name="evaluation.profile",
                    message="Evaluated profile name is required",
                    value=profile,
                ))

            eval_result = getattr(evaluation, 'result', None)
            if not eval_result or not str(eval_result).strip():
                result.add_violation(Violation(
                    level=ViolationLevel.STRUCTURAL,
                    field_name="evaluation.result",
                    message="Evaluation result (ACCEPTED/REJECTED) is required",
                    value=eval_result,
                ))


    def _check_lexical(self, candidate, result: ValidationResult):
        email = getattr(candidate, 'email', '')
        if email and not EMAIL_PATTERN.match(email):
            result.add_violation(Violation(
                level=ViolationLevel.LEXICAL,
                field_name="email",
                message="Email does not match the expected lexical pattern",
                value=email,
            ))

        skills = getattr(candidate, 'skills', [])
        for skill in skills:
            skill_str = _skill_text(skill)
            if not CANONICAL_SKILL_PATTERN.match(skill_str):
                result.add_violation(Violation(
                    level=ViolationLevel.LEXICAL,
                    field_name="skill",
                    message=(
                        "Skill token must be in canonical form "
                        "(uppercase letters, digits, underscores)"
                    ),
                    value=skill_str,
                ))

        skill_set = set()
        for skill in skills:
            skill_str = _skill_text(skill)
            if skill_str in skill_set:
                result.add_violation(Violation(
                    level=ViolationLevel.LEXICAL,
                    field_name="skill",
                    message="Duplicate skill token detected",
                    value=skill_str,
                ))
            skill_set.add(skill_str)

        experiences = getattr(candidate, 'experiences', [])
        for exp in experiences:
            duration = getattr(exp, 'duration', '')
            if duration and not DURATION_PATTERN.match(duration.strip()):
                result.add_violation(Violation(
                    level=ViolationLevel.LEXICAL,
                    field_name="experience.duration",
                    message=(
                        "Duration must match pattern "
                        "'<number> years' or '<number> months'"
                    ),
                    value=duration,
                ))

    def _check_semantic(self, candidate, result: ValidationResult):
        evaluation = getattr(candidate, 'evaluation', None)
        if evaluation is None:
            return

        profile = getattr(evaluation, 'profile', '')
        if profile and profile.strip() not in self.valid_profiles:
            result.add_violation(Violation(
                level=ViolationLevel.SEMANTIC,
                field_name="evaluation.profile",
                message=(
                    f"Profile must be one of: "
                    f"{', '.join(self.valid_profiles)}"
                ),
                value=profile,
            ))

        eval_result = str(getattr(evaluation, 'result', '')).strip()
        if eval_result and eval_result not in VALID_RESULTS:
            result.add_violation(Violation(
                level=ViolationLevel.SEMANTIC,
                field_name="evaluation.result",
                message=f"Result must be one of: {', '.join(VALID_RESULTS)}",
                value=eval_result,
            ))

        if eval_result == "ACCEPTED":
            skills = getattr(candidate, 'skills', [])
            if len(skills) < 3:
                result.add_violation(Violation(
                    level=ViolationLevel.SEMANTIC,
                    field_name="evaluation.result",
                    message=(
                        "Profile marked as ACCEPTED but has fewer than "
                        "3 skills — likely inconsistent with the profile pattern"
                    ),
                    value=f"{len(skills)} skills",
                ))

class ProfileRejectionError(Exception):
    def __init__(self, validation_result: ValidationResult):
        self.validation_result = validation_result
        super().__init__(validation_result.summary())