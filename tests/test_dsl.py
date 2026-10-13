

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from textx.exceptions import TextXSyntaxError

from dsl.parser import ResumeParser
from dsl.validator import (
    ProfileRejectionError,
    ProfileValidator,
    ViolationLevel,
)

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'samples', 'candidates')


def levels(result):
    return {v.level for v in result.violations}


def fields(result):
    return {v.field_name for v in result.violations}


class TestParser:

    def test_parses_valid_profile_string(self, parser, build_text):
        candidate = parser.parse_string(build_text())

        assert candidate.name == "Test User"
        assert candidate.email == "test@example.com"
        assert len(candidate.skills) == 5
        assert candidate.evaluation.profile == "Full Stack Developer"
        assert candidate.evaluation.result == "ACCEPTED"

    def test_parses_skills_in_order(self, parser, build_text):
        candidate = parser.parse_string(
            build_text(skills=["JAVASCRIPT", "REACT", "NODE_JS"])
        )
        assert [str(s.value) for s in candidate.skills] == [
            "JAVASCRIPT", "REACT", "NODE_JS"
        ]

    def test_parses_experiences(self, parser, build_text):
        candidate = parser.parse_string(build_text(experiences=[
            {
                "company": "Acme Corp",
                "duration": "2 years",
                "description": "Built web applications",
            },
        ]))

        assert len(candidate.experiences) == 1
        assert candidate.experiences[0].company == "Acme Corp"
        assert candidate.experiences[0].duration == "2 years"

    def test_parses_sample_resume_file(self, parser):
        path = os.path.join(SAMPLES_DIR, 'wednesday_addams.resume')
        candidate = parser.parse_file(path)

        assert candidate.name == "Wednesday Addams"
        assert candidate.evaluation.result == "ACCEPTED"
        assert len(candidate.skills) == 5

    def test_missing_file_raises(self, parser):
        with pytest.raises(FileNotFoundError):
            parser.parse_file(os.path.join(SAMPLES_DIR, 'does_not_exist.resume'))

    def test_syntax_error_raises(self, parser):
        malformed = """
        CandidateProfile {
            name: "Broken"
            email: "broken@example.com"
        """
        with pytest.raises(TextXSyntaxError):
            parser.parse_string(malformed)

    def test_unknown_field_raises(self, parser):
        malformed = """
        CandidateProfile {
            name: "Broken"
            nickname: "nope"
        }
        """
        with pytest.raises(TextXSyntaxError):
            parser.parse_string(malformed)

    def test_validate_candidate_accepts_complete_profile(self, parser, build_text):
        candidate = parser.parse_string(build_text())
        assert parser.validate_candidate(candidate) is True

    def test_validate_candidate_rejects_incomplete_profile(self, parser):
        candidate = parser.parse_string("CandidateProfile { }")
        with pytest.raises(ValueError):
            parser.validate_candidate(candidate)

    def test_summary_reports_expected_fields(self, parser, build_text):
        summary = parser.get_candidate_summary(
            parser.parse_string(build_text(skills=["PYTHON", "GIT"]))
        )

        assert summary["name"] == "Test User"
        assert summary["skills_count"] == 2
        assert summary["profile_evaluated"] == "Full Stack Developer"
        assert summary["pattern_result"] == "ACCEPTED"


class TestValidator:

    def test_valid_profile_passes(self, parser, validator, build_text):
        candidate = parser.parse_string(build_text())
        result = validator.validate(candidate)

        assert result.is_valid
        assert result.violations == []
        assert result.candidate_name == "Test User"

    def test_missing_structural_fields_are_reported(self, parser, validator):
        candidate = parser.parse_string("CandidateProfile { }")
        result = validator.validate(candidate)

        assert not result.is_valid
        assert ViolationLevel.STRUCTURAL in levels(result)
        assert {"name", "email", "skills", "evaluation"} <= fields(result)

    def test_invalid_email_is_reported(self, parser, validator, build_text):
        candidate = parser.parse_string(build_text(email="not-an-email"))
        result = validator.validate(candidate)

        assert not result.is_valid
        assert ViolationLevel.LEXICAL in levels(result)
        assert "email" in fields(result)

    def test_lowercase_skill_is_reported(self, parser, validator, build_text):
        candidate = parser.parse_string(
            build_text(skills=["python", "JAVASCRIPT", "GIT"])
        )
        result = validator.validate(candidate)

        assert not result.is_valid
        assert result.violations[0].value == "python"

    def test_duplicate_skills_are_reported(self, parser, validator, build_text):
        candidate = parser.parse_string(
            build_text(skills=["PYTHON", "PYTHON", "GIT"])
        )
        result = validator.validate(candidate)

        assert not result.is_valid
        assert any("Duplicate" in v.message for v in result.violations)

    def test_invalid_duration_is_reported(self, parser, validator, build_text):
        candidate = parser.parse_string(build_text(experiences=[
            {
                "company": "Acme Corp",
                "duration": "three years",
                "description": "Built things",
            },
        ]))
        result = validator.validate(candidate)

        assert not result.is_valid
        assert "experience.duration" in fields(result)

    def test_unknown_profile_is_rejected(self, parser, validator, build_text):
        candidate = parser.parse_string(build_text(profile="Blockchain Developer"))
        result = validator.validate(candidate)

        assert not result.is_valid
        assert ViolationLevel.SEMANTIC in levels(result)
        assert "evaluation.profile" in fields(result)

    def test_accepted_result_with_too_few_skills_is_rejected(
        self, parser, validator, build_text
    ):
        candidate = parser.parse_string(build_text(skills=["PYTHON"]))
        result = validator.validate(candidate)

        assert not result.is_valid
        assert "evaluation.result" in fields(result)

    def test_rejected_result_with_few_skills_is_valid(
        self, parser, validator, build_text
    ):
        candidate = parser.parse_string(
            build_text(skills=["PYTHON"], result="REJECTED")
        )
        result = validator.validate(candidate)

        assert result.is_valid

    def test_validate_or_raise_raises_profile_rejection(
        self, parser, validator, build_text
    ):
        candidate = parser.parse_string(build_text(profile="Blockchain Developer"))

        with pytest.raises(ProfileRejectionError) as exc:
            validator.validate_or_raise(candidate)

        assert not exc.value.validation_result.is_valid

    def test_validate_or_raise_returns_result_when_valid(
        self, parser, validator, build_text
    ):
        candidate = parser.parse_string(build_text())
        result = validator.validate_or_raise(candidate)

        assert result.is_valid

    def test_validation_summary_mentions_rejection(self, parser, validator, build_text):
        candidate = parser.parse_string(build_text(profile="Blockchain Developer"))
        summary = validator.validate(candidate).summary()

        assert "REJECTED" in summary
        assert "Blockchain Developer" in summary or "Test User" in summary


class TestParserAndValidatorTogether:

    def test_validate_and_report_returns_result(self, parser, build_text):
        candidate = parser.parse_string(build_text())
        result = parser.validate_and_report(candidate)

        assert result.is_valid

    def test_end_to_end_rejects_invalid_candidate(self, parser, build_text):
        candidate = parser.parse_string(build_text(
            email="bad-email",
            profile="Blockchain Developer",
            skills=["python"],
        ))
        result = parser.validate_and_report(candidate)

        assert not result.is_valid
        assert {ViolationLevel.LEXICAL, ViolationLevel.SEMANTIC} <= levels(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
