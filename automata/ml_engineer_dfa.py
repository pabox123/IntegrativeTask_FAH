from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State


def create_ml_engineer_dfa():
    """
    states:
    - q0: initial state
    - q1: programming language qualification seen
    - q2: data processing qualification seen
    - q3: ML libraries qualification seen
    - q4: deep learning qualification seen
    - q5: database qualification seen
    - q6: version control qualification seen (accepting state)
    - q_reject: reject state
    """

    q0 = State("q0")
    q1 = State("q1")
    q2 = State("q2")
    q3 = State("q3")
    q4 = State("q4")
    q5 = State("q5")
    q6 = State("q6")
    q_reject = State("q_reject")

    dfa = DeterministicFiniteAutomaton()

    dfa.add_start_state(q0)
    dfa.add_final_state(q6)

    # q0 -> q1: programming languages
    programming_languages = ["PYTHON", "R"]
    for skill in programming_languages:
        dfa.add_transition(q0, skill, q1)

    # from q0 goes to reject
    dfa.add_transition(q0, "OTHER", q_reject)

    # q1 -> q2: data processing libraries
    data_processing = ["PANDAS", "NUMPY"]
    for skill in data_processing:
        dfa.add_transition(q1, skill, q2)

    # stay in q1 if more programming languages appear
    for skill in programming_languages:
        dfa.add_transition(q1, skill, q1)

    # from q1 goes to reject
    dfa.add_transition(q1, "OTHER", q_reject)

    # q2 -> q3: ML libraries
    ml_libraries = ["SCIKIT_LEARN", "XGBOOST"]
    for skill in ml_libraries:
        dfa.add_transition(q2, skill, q3)

    # stay in q2 or go back to q1
    for skill in data_processing:
        dfa.add_transition(q2, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q2, skill, q1)

    # from q2 goes to reject
    dfa.add_transition(q2, "OTHER", q_reject)

    # q3 -> q4: deep learning frameworks
    deep_learning = ["TENSORFLOW", "PYTORCH"]
    for skill in deep_learning:
        dfa.add_transition(q3, skill, q4)

    # stay in q3 or go back to previous states
    for skill in ml_libraries:
        dfa.add_transition(q3, skill, q3)
    for skill in data_processing:
        dfa.add_transition(q3, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q3, skill, q1)

    # from q3 goes to reject
    dfa.add_transition(q3, "OTHER", q_reject)

    # q4 -> q5: databases
    databases = ["SQL", "POSTGRESQL", "MYSQL", "BIGQUERY"]
    for skill in databases:
        dfa.add_transition(q4, skill, q5)

    # stay in q4 or go back to previous states
    for skill in deep_learning:
        dfa.add_transition(q4, skill, q4)
    for skill in ml_libraries:
        dfa.add_transition(q4, skill, q3)
    for skill in data_processing:
        dfa.add_transition(q4, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q4, skill, q1)

    # from q4 goes to reject
    dfa.add_transition(q4, "OTHER", q_reject)

    # q5 -> q6: version control
    version_control = ["GIT"]
    for skill in version_control:
        dfa.add_transition(q5, skill, q6)

    # stay in q5 or go back to previous states
    for skill in databases:
        dfa.add_transition(q5, skill, q5)
    for skill in deep_learning:
        dfa.add_transition(q5, skill, q4)
    for skill in ml_libraries:
        dfa.add_transition(q5, skill, q3)
    for skill in data_processing:
        dfa.add_transition(q5, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q5, skill, q1)

    # from q5 goes to reject
    dfa.add_transition(q5, "OTHER", q_reject)

    # q6: accepting state - all skills can repeat
    all_skills = (
            programming_languages
            + data_processing
            + ml_libraries
            + deep_learning
            + databases
            + version_control
    )
    for skill in all_skills:
        dfa.add_transition(q6, skill, q6)

    # reject state: loops to itself
    dfa.add_transition(q_reject, "OTHER", q_reject)

    return dfa


def validate_ml_engineer_profile(qualifications_sequence):

    dfa = create_ml_engineer_dfa()
    symbols = list(qualifications_sequence)
    return dfa.accepts(symbols)


def get_ml_engineer_profile_info():
    return {
        "profile_name": "Machine Learning Engineer",
        "description": (
            "Combines software development, data processing, and "
            "machine-learning techniques to build computational systems "
            "that use predictive or learning-based models"
        ),
        "canonical_order": [
            "Programming Language",
            "Data Processing",
            "ML Libraries",
            "Deep Learning",
            "Database",
            "Version Control",
        ],
        "requirements": {
            "Programming Language": ["PYTHON", "R"],
            "Data Processing": ["PANDAS", "NUMPY"],
            "ML Libraries": ["SCIKIT_LEARN", "XGBOOST"],
            "Deep Learning": ["TENSORFLOW", "PYTORCH"],
            "Database": ["SQL", "POSTGRESQL", "MYSQL", "BIGQUERY"],
            "Version Control": ["GIT"],
        },
        "pattern": (
            "Programming Language -> Data Processing -> ML Libraries "
            "-> Deep Learning -> Database -> Version Control"
        ),
    }


if __name__ == "__main__":
    # test 1
    valid_sequence = [
        "PYTHON", "PANDAS", "SCIKIT_LEARN",
        "TENSORFLOW", "POSTGRESQL", "GIT"
    ]
    print(f"Sequence: {valid_sequence}")
    print(f"Accepted: {validate_ml_engineer_profile(valid_sequence)}")
    print()

    # test 2
    valid_sequence_2 = [
        "R", "NUMPY", "XGBOOST",
        "PYTORCH", "SQL", "GIT"
    ]
    print(f"Sequence: {valid_sequence_2}")
    print(f"Accepted: {validate_ml_engineer_profile(valid_sequence_2)}")
    print()

    # test 3
    invalid_sequence = [
        "PYTHON", "PANDAS", "SCIKIT_LEARN",
        "POSTGRESQL", "GIT"
    ]
    print(f"Sequence: {invalid_sequence}")
    print(f"Accepted: {validate_ml_engineer_profile(invalid_sequence)}")
    print()

    # test 4
    invalid_sequence_2 = [
        "PYTHON", "PANDAS", "TENSORFLOW",
        "SCIKIT_LEARN", "SQL", "GIT"
    ]
    print(f"Sequence: {invalid_sequence_2}")
    print(f"Accepted: {validate_ml_engineer_profile(invalid_sequence_2)}")
    print()

    # test 5
    invalid_sequence_3 = [
        "PANDAS", "SCIKIT_LEARN", "TENSORFLOW",
        "SQL", "GIT"
    ]
    print(f"Sequence: {invalid_sequence_3}")
    print(f"Accepted: {validate_ml_engineer_profile(invalid_sequence_3)}")