from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State


def create_devops_dfa():
    """
    states:
    - q0: initial state
    - q1: programming/scripting qualification seen
    - q2: containers qualification seen
    - q3: CI/CD qualification seen
    - q4: infrastructure as code qualification seen
    - q5: cloud qualification seen
    - q6: monitoring qualification seen
    - q7: version control qualification seen
    - q_reject: reject state
    """

    q0 = State("q0")
    q1 = State("q1")
    q2 = State("q2")
    q3 = State("q3")
    q4 = State("q4")
    q5 = State("q5")
    q6 = State("q6")
    q7 = State("q7")
    q_reject = State("q_reject")

    dfa = DeterministicFiniteAutomaton()

    dfa.add_start_state(q0)
    dfa.add_final_state(q7)

    # q0 -> q1 programming languages
    programming = ["PYTHON", "BASH", "POWERSHELL"]
    for skill in programming:
        dfa.add_transition(q0, skill, q1)

    # from q0 goes to reject
    dfa.add_transition(q0, "OTHER", q_reject)

    # q1 -> q2 containers
    containers = ["DOCKER", "KUBERNETES", "HELM"]
    for skill in containers:
        dfa.add_transition(q1, skill, q2)

    # stay in q1 if more programming languages appear
    for skill in programming:
        dfa.add_transition(q1, skill, q1)

    # from q1 goes to reject
    dfa.add_transition(q1, "OTHER", q_reject)

    # q2 -> q3 CI/CD tools
    cicd = ["JENKINS", "GITLAB_CI", "GITHUB_ACTIONS"]
    for skill in cicd:
        dfa.add_transition(q2, skill, q3)

    # stay in q2 or go back to q1
    for skill in containers:
        dfa.add_transition(q2, skill, q2)
    for skill in programming:
        dfa.add_transition(q2, skill, q1)

    # from q2 goes to reject
    dfa.add_transition(q2, "OTHER", q_reject)

    # q3 -> q4 infrastructure as code
    iac = ["TERRAFORM", "ANSIBLE", "CLOUDFORMATION"]
    for skill in iac:
        dfa.add_transition(q3, skill, q4)

    # stay in q3 or go to previous states
    for skill in cicd:
        dfa.add_transition(q3, skill, q3)
    for skill in containers:
        dfa.add_transition(q3, skill, q2)
    for skill in programming:
        dfa.add_transition(q3, skill, q1)

    # from q3 goes to reject
    dfa.add_transition(q3, "OTHER", q_reject)

    # q4 -> q5 cloud platforms
    cloud = ["AWS", "AZURE", "GCP"]
    for skill in cloud:
        dfa.add_transition(q4, skill, q5)

    # stay in q4 or go to previous states
    for skill in iac:
        dfa.add_transition(q4, skill, q4)
    for skill in cicd:
        dfa.add_transition(q4, skill, q3)
    for skill in containers:
        dfa.add_transition(q4, skill, q2)
    for skill in programming:
        dfa.add_transition(q4, skill, q1)

    # from q4 goes to reject
    dfa.add_transition(q4, "OTHER", q_reject)

    # q5 -> q6 monitoring tools
    monitoring = ["PROMETHEUS", "GRAFANA", "ELK"]
    for skill in monitoring:
        dfa.add_transition(q5, skill, q6)

    # stay in q5 or go to previous states
    for skill in cloud:
        dfa.add_transition(q5, skill, q5)
    for skill in iac:
        dfa.add_transition(q5, skill, q4)
    for skill in cicd:
        dfa.add_transition(q5, skill, q3)
    for skill in containers:
        dfa.add_transition(q5, skill, q2)
    for skill in programming:
        dfa.add_transition(q5, skill, q1)

    # from q5 goes to reject
    dfa.add_transition(q5, "OTHER", q_reject)

    # q6 -> q7 version control
    version_control = ["GIT"]
    for skill in version_control:
        dfa.add_transition(q6, skill, q7)

    # stay in q6 or go back to previous states
    for skill in monitoring:
        dfa.add_transition(q6, skill, q6)
    for skill in cloud:
        dfa.add_transition(q6, skill, q5)
    for skill in iac:
        dfa.add_transition(q6, skill, q4)
    for skill in cicd:
        dfa.add_transition(q6, skill, q3)
    for skill in containers:
        dfa.add_transition(q6, skill, q2)
    for skill in programming:
        dfa.add_transition(q6, skill, q1)

    # from q6 goes to reject
    dfa.add_transition(q6, "OTHER", q_reject)

    # q7 accepting state when all skills can repeat
    all_skills = (
            programming
            + containers
            + cicd
            + iac
            + cloud
            + monitoring
            + version_control
    )
    for skill in all_skills:
        dfa.add_transition(q7, skill, q7)

    # finally reject state loops to itself
    dfa.add_transition(q_reject, "OTHER", q_reject)
    return dfa

def validate_devops_profile(qualifications_sequence):

    dfa = create_devops_dfa()
    symbols = list(qualifications_sequence)
    return dfa.accepts(symbols)


def get_devops_profile_info():
    return {
        "profile_name": "DevOps Engineer",
        "description": (
            "Automates infrastructure, CI/CD pipelines, and deployment "
            "processes for cloud-native applications. Expert in container "
            "orchestration and infrastructure as code."
        ),
        "canonical_order": [
            "Programming/Scripting",
            "Containers",
            "CI/CD",
            "Infrastructure as Code",
            "Cloud",
            "Monitoring",
            "Version Control",
        ],
        "requirements": {
            "Programming/Scripting": ["PYTHON", "BASH", "POWERSHELL"],
            "Containers": ["DOCKER", "KUBERNETES", "HELM"],
            "CI/CD": ["JENKINS", "GITLAB_CI", "GITHUB_ACTIONS"],
            "Infrastructure as Code": ["TERRAFORM", "ANSIBLE", "CLOUDFORMATION"],
            "Cloud": ["AWS", "AZURE", "GCP"],
            "Monitoring": ["PROMETHEUS", "GRAFANA", "ELK"],
            "Version Control": ["GIT"],
        },
        "pattern": (
            "Programming/Scripting -> Containers -> CI/CD -> Infrastructure as Code "
            "-> Cloud -> Monitoring -> Version Control"
        ),
    }


if __name__ == "__main__":
    # test 1
    valid_sequence = [
        "PYTHON", "DOCKER", "JENKINS",
        "TERRAFORM", "AWS", "PROMETHEUS", "GIT"
    ]
    print(f"Sequence: {valid_sequence}")
    print(f"Accepted: {validate_devops_profile(valid_sequence)}")
    print()

    # test 2
    valid_sequence_2 = [
        "BASH", "KUBERNETES", "GITLAB_CI",
        "ANSIBLE", "AZURE", "GRAFANA", "GIT"
    ]
    print(f"Sequence: {valid_sequence_2}")
    print(f"Accepted: {validate_devops_profile(valid_sequence_2)}")
    print()

    # test 3
    invalid_sequence = [
        "PYTHON", "DOCKER", "JENKINS",
        "TERRAFORM", "AWS", "GIT"
    ]
    print(f"Sequence: {invalid_sequence}")
    print(f"Accepted: {validate_devops_profile(invalid_sequence)}")
    print()

    # test 4
    invalid_sequence_2 = [
        "PYTHON", "DOCKER", "AWS",
        "JENKINS", "TERRAFORM", "PROMETHEUS", "GIT"
    ]
    print(f"Sequence: {invalid_sequence_2}")
    print(f"Accepted: {validate_devops_profile(invalid_sequence_2)}")
    print()

    # test 5
    invalid_sequence_3 = [
        "DOCKER", "JENKINS", "TERRAFORM",
        "AWS", "PROMETHEUS", "GIT"
    ]
    print(f"Sequence: {invalid_sequence_3}")
    print(f"Accepted: {validate_devops_profile(invalid_sequence_3)}")