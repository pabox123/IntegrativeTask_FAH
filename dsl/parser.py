

from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError, TextXSemanticError
import os


class ResumeParser:

    def __init__(self, grammar_path=None):
        if grammar_path is None:

            current_dir = os.path.dirname(os.path.abspath(__file__))
            grammar_path = os.path.join(current_dir, 'resume_dsl.tx')

        self.grammar_path = grammar_path

        try:
            self.metamodel = metamodel_from_file(self.grammar_path)
            print(f"✓ Grammar loaded successfully from {self.grammar_path}")
        except Exception as e:
            raise ValueError(f"Error loading grammar: {e}")

    def parse_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            candidate = self.metamodel.model_from_file(file_path)
            print(f"✓ Successfully parsed: {file_path}")
            return candidate
        except TextXSyntaxError as e:
            print(f"✗ Syntax error in {file_path}:")
            print(f"  Line {e.line}, Column {e.col}: {e.message}")
            raise
        except TextXSemanticError as e:
            print(f"✗ Semantic error in {file_path}:")
            print(f"  {e.message}")
            raise

    def parse_string(self, text):
        try:
            candidate = self.metamodel.model_from_str(text)
            print("✓ Successfully parsed candidate profile from string")
            return candidate
        except TextXSyntaxError as e:
            print(f"✗ Syntax error:")
            print(f"  Line {e.line}, Column {e.col}: {e.message}")
            raise
        except TextXSemanticError as e:
            print(f"✗ Semantic error:")
            print(f"  {e.message}")
            raise

    def validate_candidate(self, candidate):
        errors = []

        if not hasattr(candidate, 'name') or not candidate.name:
            errors.append("Missing candidate name")

        if not hasattr(candidate, 'email') or not candidate.email:
            errors.append("Missing email")

        if not hasattr(candidate, 'skills') or len(candidate.skills) == 0:
            errors.append("Candidate must have at least one technical skill")

        if not hasattr(candidate, 'evaluation') or not candidate.evaluation:
            errors.append("Missing qualification evaluation")

        if errors:
            error_msg = "Validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(error_msg)

        print("✓ Candidate profile validation passed")
        return True

    def get_candidate_summary(self, candidate):
        summary = {
            'name': candidate.name if hasattr(candidate, 'name') else 'Unknown',
            'email': candidate.email if hasattr(candidate, 'email') else 'Unknown',
            'location': candidate.location if hasattr(candidate, 'location') else 'Unknown',
            'skills_count': len(candidate.skills) if hasattr(candidate, 'skills') else 0,
            'experience_count': len(candidate.experiences) if hasattr(candidate, 'experiences') else 0,
            'profile_evaluated': candidate.evaluation.profile if hasattr(candidate, 'evaluation') else 'Unknown',
            'pattern_result': candidate.evaluation.result if hasattr(candidate, 'evaluation') else 'Unknown'
        }

        return summary

    def validate_and_report(self, candidate):
        try:
            from dsl.validator import ProfileValidator
        except ModuleNotFoundError:
            # Allow running this file directly (python dsl/parser.py)
            from validator import ProfileValidator

        validator = ProfileValidator()
        result = validator.validate(candidate)

        print("\n" + result.summary())
        return result

def main():
    parser = ResumeParser()

    print("\n" + "="*60)
    print("Example 1: Parsing from file")
    print("="*60)

    try:
        candidate = parser.parse_file('samples/candidates/wednesday_addams.resume')
        parser.validate_candidate(candidate)
        summary = parser.get_candidate_summary(candidate)
        print("\nCandidate Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*60)
    print("Example 2: Parsing from string")
    print("="*60)

    candidate_text = """
    CandidateProfile {
        name: "Mary Jane Watson"
        email: "mj.watson@example.com"
        location: "New York, USA"
        current_role: "Machine Learning Engineer"
        
        summary: "2 years of experience developing predictive models"
        
        Experience {
            company: "Daily Bugle Tech"
            duration: "2 years"
            description: "Developed ML models for content recommendation"
        }
        
        Skill: PYTHON
        Skill: PANDAS
        Skill: SCIKIT_LEARN
        Skill: TENSORFLOW
        Skill: SQL
        Skill: GIT
        
        Evaluation {
            profile: "Machine Learning Engineer"
            result: ACCEPTED
            description: "The normalized qualifications satisfy an accepted ML Engineer pattern"
        }
    }
    """

    try:
        candidate = parser.parse_string(candidate_text)
        parser.validate_candidate(candidate)
        summary = parser.get_candidate_summary(candidate)
        print("\nCandidate Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

    # example 3
    print("\n" + "="*60)
    print("Example 3: Parsing and rejecting invalid candidate")
    print("="*60)

    invalid_text = """
    CandidateProfile {
        name: ""
        email: "not-an-email"
        location: "Unknown"

        Skill: python
        Skill: JAVASCRIPT
        Skill: JAVASCRIPT

        Evaluation {
            profile: "Blockchain Developer"
            result: ACCEPTED
            description: "This should be rejected"
        }
    }
    """

    try:
        candidate = parser.parse_string(invalid_text)
        result = parser.validate_and_report(candidate)

        if not result.is_valid:
            print("\n⚠ Candidate REJECTED — see violations above.")
    except Exception as e:
        print(f"\nParsing error: {type(e).__name__}: {e}")

    try:
        candidate = parser.parse_string(invalid_text)
        parser.validate_candidate(candidate)
    except Exception as e:
        print(f"\nExpected error caught: {type(e).__name__}")


if __name__ == "__main__":
    main()