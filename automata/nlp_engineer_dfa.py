from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State


def create_nlp_engineer_dfa():
    """
    states:
    - q0: initial state
    - q1: programming language qualification seen
    - q2: NLP libraries qualification seen
    - q3: deep learning for NLP qualification seen
    - q4: pre-trained models qualification seen
    - q5: database qualification seen
    - q6: tools qualification seen
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

    # q0 -> q1 programming languages
    programming_languages = ["PYTHON", "SQL", "BASH"]
    for skill in programming_languages:
        dfa.add_transition(q0, skill, q1)

    # from q0 goes to reject
    dfa.add_transition(q0, "OTHER", q_reject)

    # q1 -> q2 nlp  libraries
    nlp_libraries = ["SPACY", "NLTK", "GENSIM"]
    for skill in nlp_libraries:
        dfa.add_transition(q1, skill, q2)

    # stay in q1 if more programming languages appear
    for skill in programming_languages:
        dfa.add_transition(q1, skill, q1)

    # from q1 goes to reject
    dfa.add_transition(q1, "OTHER", q_reject)

    # q2 -> q3 deep learning for nlp
    deep_learning = ["PYTORCH", "TENSORFLOW", "TRANSFORMERS"]
    for skill in deep_learning:
        dfa.add_transition(q2, skill, q3)

    # stay in q2 or go to q1
    for skill in nlp_libraries:
        dfa.add_transition(q2, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q2, skill, q1)

    # from q2 goes to reject
    dfa.add_transition(q2, "OTHER", q_reject)

    # q3 -> q4 pre trained models
    pretrained_models = ["BERT", "ROBERTA"]
    for skill in pretrained_models:
        dfa.add_transition(q3, skill, q4)

    # stay in q3 or go to previous states
    for skill in deep_learning:
        dfa.add_transition(q3, skill, q3)
    for skill in nlp_libraries:
        dfa.add_transition(q3, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q3, skill, q1)

    # from q3 goes to reject
    dfa.add_transition(q3, "OTHER", q_reject)

    # q4 -> q5 databases
    databases = ["POSTGRESQL", "MYSQL", "ELASTICSEARCH"]
    for skill in databases:
        dfa.add_transition(q4, skill, q5)

    # stay in q4 or go to previous states
    for skill in pretrained_models:
        dfa.add_transition(q4, skill, q4)
    for skill in deep_learning:
        dfa.add_transition(q4, skill, q3)
    for skill in nlp_libraries:
        dfa.add_transition(q4, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q4, skill, q1)

    # from q4 goes to reject
    dfa.add_transition(q4, "OTHER", q_reject)

    # q5 -> q6 tools
    tools = ["DOCKER", "GIT", "JUPYTER", "FASTAPI"]
    for skill in tools:
        dfa.add_transition(q5, skill, q6)

    # stay in q5 or go to previous states
    for skill in databases:
        dfa.add_transition(q5, skill, q5)
    for skill in pretrained_models:
        dfa.add_transition(q5, skill, q4)
    for skill in deep_learning:
        dfa.add_transition(q5, skill, q3)
    for skill in nlp_libraries:
        dfa.add_transition(q5, skill, q2)
    for skill in programming_languages:
        dfa.add_transition(q5, skill, q1)

    # from q5 goes to reject
    dfa.add_transition(q5, "OTHER", q_reject)

    # q6 all skills can repeat
    all_skills = (
            programming_languages
            + nlp_libraries
            + deep_learning
            + pretrained_models
            + databases
            + tools
    )
    for skill in all_skills:
        dfa.add_transition(q6, skill, q6)

    # loops to itself rejecting state
    dfa.add_transition(q_reject, "OTHER", q_reject)

    return dfa


def validate_nlp_engineer_profile(qualifications_sequence):

    dfa = create_nlp_engineer_dfa()
    symbols = list(qualifications_sequence)
    return dfa.accepts(symbols)

def get_nlp_engineer_profile_info():
    return {
        "profile_name": "NLP Engineer",
        "description": (
            "Builds language models and text processing systems. "
            "Specialized in transformer architectures and multilingual "
            "NLP for real-world applications."
        ),
        "canonical_order": [
            "Programming Language",
            "NLP Libraries",
            "Deep Learning for NLP",
            "Pre-trained Models",
            "Database",
            "Tools",
        ],
        "requirements": {
            "Programming Language": ["PYTHON", "SQL", "BASH"],
            "NLP Libraries": ["SPACY", "NLTK", "GENSIM"],
            "Deep Learning for NLP": ["PYTORCH", "TENSORFLOW", "TRANSFORMERS"],
            "Pre-trained Models": ["BERT", "ROBERTA"],
            "Database": ["POSTGRESQL", "MYSQL", "ELASTICSEARCH"],
            "Tools": ["DOCKER", "GIT", "JUPYTER", "FASTAPI"],
        },
        "pattern": (
            "Programming Language -> NLP Libraries -> Deep Learning for NLP "
            "-> Pre-trained Models -> Database -> Tools"
        ),
    }


if __name__ == "__main__":
    # test 1
    valid_sequence = [
        "PYTHON", "SPACY", "PYTORCH",
        "BERT", "POSTGRESQL", "GIT"
    ]
    print(f"Sequence: {valid_sequence}")
    print(f"Accepted: {validate_nlp_engineer_profile(valid_sequence)}")
    print()

    # test 2
    valid_sequence_2 = [
        "SQL", "NLTK", "TRANSFORMERS",
        "ROBERTA", "ELASTICSEARCH", "DOCKER"
    ]
    print(f"Sequence: {valid_sequence_2}")
    print(f"Accepted: {validate_nlp_engineer_profile(valid_sequence_2)}")
    print()

    # test 3
    invalid_sequence = [
        "PYTHON", "SPACY", "PYTORCH",
        "POSTGRESQL", "GIT"
    ]
    print(f"Sequence: {invalid_sequence}")
    print(f"Accepted: {validate_nlp_engineer_profile(invalid_sequence)}")
    print()

    # test 4
    invalid_sequence_2 = [
        "PYTHON", "SPACY", "BERT",
        "PYTORCH", "POSTGRESQL", "GIT"
    ]
    print(f"Sequence: {invalid_sequence_2}")
    print(f"Accepted: {validate_nlp_engineer_profile(invalid_sequence_2)}")
    print()

    # test 5
    invalid_sequence_3 = [
        "SPACY", "PYTORCH", "BERT",
        "POSTGRESQL", "GIT"
    ]
    print(f"Sequence: {invalid_sequence_3}")
    print(f"Accepted: {validate_nlp_engineer_profile(invalid_sequence_3)}")