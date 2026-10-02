import os

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State


def create_full_stack_dfa():
    """
    States:
    - q0: initial state
    - q1: frontend qualification seen
    - q2: backend qualification seen
    - q3: database qualification seen
    - q4: version control qualification seen
    - q_reject: reject state
    """

    q0 = State("q0")
    q1 = State("q1")
    q2 = State("q2")
    q3 = State("q3")
    q4 = State("q4")
    q_reject = State("q_reject")

    dfa = DeterministicFiniteAutomaton()

    # Start and accepting states (the other states are registered
    # automatically when they are used in a transition)
    dfa.add_start_state(q0)
    dfa.add_final_state(q4)

    # only frontend qualifications are valid
    frontend_skills = ["JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE"]
    for skill in frontend_skills:
        dfa.add_transition(q0, skill, q1)

    #from q0 goes to reject
    dfa.add_transition(q0, "OTHER", q_reject)

    #  backend qualifications are valid
    backend_skills = ["NODE_JS", "DJANGO", "SPRING_BOOT", "EXPRESS"]
    for skill in backend_skills:
        dfa.add_transition(q1, skill, q2)

    for skill in frontend_skills:
        dfa.add_transition(q1, skill, q1)

    # from q1 goes to reject
    dfa.add_transition(q1, "OTHER", q_reject)

    # database qualifications are valid
    database_skills = ["POSTGRESQL", "MYSQL", "MONGODB", "SQL", "NOSQL"]
    for skill in database_skills:
        dfa.add_transition(q2, skill, q3)

    # stay in q2 or go back to q1
    for skill in backend_skills:
        dfa.add_transition(q2, skill, q2)
    for skill in frontend_skills:
        dfa.add_transition(q2, skill, q1)

    # from q2 goes to reject
    dfa.add_transition(q2, "OTHER", q_reject)

    # version control qualifications are valid
    version_control_skills = ["GIT"]
    for skill in version_control_skills:
        dfa.add_transition(q3, skill, q4)


    for skill in database_skills:
        dfa.add_transition(q3, skill, q3)
    for skill in backend_skills:
        dfa.add_transition(q3, skill, q2)
    for skill in frontend_skills:
        dfa.add_transition(q3, skill, q1)


    dfa.add_transition(q3, "OTHER", q_reject)

    # all skills can repeat, stay in q4
    all_skills = frontend_skills + backend_skills + database_skills + version_control_skills
    for skill in all_skills:
        dfa.add_transition(q4, skill, q4)


    dfa.add_transition(q_reject, "OTHER", q_reject)

    return dfa


def validate_full_stack_profile(qualifications_sequence):

    dfa = create_full_stack_dfa()

    symbols = list(qualifications_sequence)

    return dfa.accepts(symbols)


def get_full_stack_profile_info():
    return {
        "profile_name": "Full Stack Developer",
        "description": "Works with both client-side and server-side components of software applications",
        "canonical_order": [
            "Frontend",
            "Backend",
            "Database",
            "Version Control"
        ],
        "requirements": {
            "Frontend": ["JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE"],
            "Backend": ["NODE_JS", "DJANGO", "SPRING_BOOT", "EXPRESS"],
            "Database": ["POSTGRESQL", "MYSQL", "MONGODB", "SQL", "NOSQL"],
            "Version Control": ["GIT"]
        },
        "pattern": "Frontend → Backend → Database → Version Control"
    }



if __name__ == "__main__":
    # test for valid full stack sequence
    valid_sequence = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    print(f"Sequence: {valid_sequence}")
    print(f"Accepted: {validate_full_stack_profile(valid_sequence)}")
    print()

    # test 2
    valid_sequence_2 = ["TYPESCRIPT", "ANGULAR", "DJANGO", "MYSQL", "GIT"]
    print(f"Sequence: {valid_sequence_2}")
    print(f"Accepted: {validate_full_stack_profile(valid_sequence_2)}")
    print()

    # test 3
    invalid_sequence = ["JAVASCRIPT", "REACT", "POSTGRESQL", "GIT"]
    print(f"Sequence: {invalid_sequence}")
    print(f"Accepted: {validate_full_stack_profile(invalid_sequence)}")
    print()

    # test 4
    invalid_sequence_2 = ["NODE_JS", "JAVASCRIPT", "REACT", "POSTGRESQL", "GIT"]
    print(f"Sequence: {invalid_sequence_2}")
    print(f"Accepted: {validate_full_stack_profile(invalid_sequence_2)}")

