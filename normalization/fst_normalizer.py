from pyformlang.fst import FST


def build_programming_languages_fst() -> FST:
    """
    Constructs an FST for normalizing programming language tokens.
    Formal Definition (7-tuple): M = (Q, Σ, Γ, δ, ω, q0, F)
    """
    fst = FST()
    fst.add_start_state('q0')

    transitions = [
        ('q0', 'JS', 'q1', ['JAVASCRIPT']),
        ('q0', 'js', 'q1', ['JAVASCRIPT']),
        ('q0', 'Js', 'q1', ['JAVASCRIPT']),
        ('q0', 'JavaScript', 'q1', ['JAVASCRIPT']),
        ('q0', 'javascript', 'q1', ['JAVASCRIPT']),
        ('q0', 'JAVASCRIPT', 'q1', ['JAVASCRIPT']),

        ('q0', 'py', 'q1', ['PYTHON']),
        ('q0', 'Py', 'q1', ['PYTHON']),
        ('q0', 'Python', 'q1', ['PYTHON']),
        ('q0', 'python', 'q1', ['PYTHON']),
        ('q0', 'PYTHON', 'q1', ['PYTHON']),

        ('q0', 'TS', 'q1', ['TYPESCRIPT']),
        ('q0', 'ts', 'q1', ['TYPESCRIPT']),
        ('q0', 'TypeScript', 'q1', ['TYPESCRIPT']),
        ('q0', 'typescript', 'q1', ['TYPESCRIPT']),
        ('q0', 'TYPESCRIPT', 'q1', ['TYPESCRIPT']),

        ('q0', 'Java', 'q1', ['JAVA']),
        ('q0', 'java', 'q1', ['JAVA']),
        ('q0', 'JAVA', 'q1', ['JAVA']),
        ('q0', 'C++', 'q1', ['CPP']),
        ('q0', 'c++', 'q1', ['CPP']),
        ('q0', 'CPP', 'q1', ['CPP']),
    ]

    fst.add_transitions(transitions)
    fst.add_final_state('q1')
    return fst


def build_frameworks_fst() -> FST:
    """
    Constructs an FST for normalizing web/backend frameworks and libraries.
    Formal Definition (7-tuple): M = (Q, Σ, Γ, δ, ω, q0, F)
    """
    fst = FST()
    fst.add_start_state('q0')

    transitions = [
        # Front
        ('q0', 'React.js', 'q1', ['REACT']),
        ('q0', 'ReactJS', 'q1', ['REACT']),
        ('q0', 'React', 'q1', ['REACT']),
        ('q0', 'react', 'q1', ['REACT']),
        ('q0', 'Vue.js', 'q1', ['VUE']),
        ('q0', 'VueJS', 'q1', ['VUE']),
        ('q0', 'Vue', 'q1', ['VUE']),
        ('q0', 'Angular', 'q1', ['ANGULAR']),
        ('q0', 'angular', 'q1', ['ANGULAR']),

        # Back
        ('q0', 'NodeJS', 'q1', ['NODE_JS']),
        ('q0', 'Node.js', 'q1', ['NODE_JS']),
        ('q0', 'Node', 'q1', ['NODE_JS']),
        ('q0', 'node', 'q1', ['NODE_JS']),
        ('q0', 'Django', 'q1', ['DJANGO']),
        ('q0', 'django', 'q1', ['DJANGO']),
        ('q0', 'Spring Boot', 'q1', ['SPRING_BOOT']),
        ('q0', 'SpringBoot', 'q1', ['SPRING_BOOT']),
        ('q0', 'Express', 'q1', ['EXPRESS']),
        ('q0', 'Express.js', 'q1', ['EXPRESS']),
        ('q0', 'REST API', 'q1', ['REST_API']),
        ('q0', 'RESTful API', 'q1', ['REST_API']),
    ]

    fst.add_transitions(transitions)
    fst.add_final_state('q1')
    return fst


def build_databases_fst() -> FST:
    """
    Constructs an FST for normalizing database engine tokens.

    Formal Definition (7-tuple): M = (Q, Σ, Γ, δ, ω, q0, F)
    - Q: {'q0', 'q1'}
    - Σ: Raw input tokens ('Postgres', 'PostgreSQL', 'MySQL', 'MongoDB', 'SQL', etc.)
    - Γ: Canonical output tokens ('POSTGRESQL', 'MYSQL', 'MONGODB', 'SQL', 'SQLITE', etc.)
    - δ: Transition relation
    - ω: Output mapping relation
    - q0: Start state 'q0'
    - F: Final accepting states {'q1'}
    """
    fst = FST()
    fst.add_start_state('q0')

    transitions = [
        ('q0', 'Postgres', 'q1', ['POSTGRESQL']),
        ('q0', 'postgres', 'q1', ['POSTGRESQL']),
        ('q0', 'PostgreSQL', 'q1', ['POSTGRESQL']),
        ('q0', 'postgresql', 'q1', ['POSTGRESQL']),
        ('q0', 'POSTGRESQL', 'q1', ['POSTGRESQL']),

        ('q0', 'MySQL', 'q1', ['MYSQL']),
        ('q0', 'mysql', 'q1', ['MYSQL']),
        ('q0', 'MYSQL', 'q1', ['MYSQL']),

        ('q0', 'MongoDB', 'q1', ['MONGODB']),
        ('q0', 'mongodb', 'q1', ['MONGODB']),
        ('q0', 'Mongo', 'q1', ['MONGODB']),
        ('q0', 'mongo', 'q1', ['MONGODB']),

        ('q0', 'SQL', 'q1', ['SQL']),
        ('q0', 'sql', 'q1', ['SQL']),
        ('q0', 'SQLite', 'q1', ['SQLITE']),
        ('q0', 'sqlite', 'q1', ['SQLITE']),

        ('q0', 'Redis', 'q1', ['REDIS']),
        ('q0', 'redis', 'q1', ['REDIS']),
        ('q0', 'MariaDB', 'q1', ['MARIADB']),
        ('q0', 'mariadb', 'q1', ['MARIADB']),
    ]

    fst.add_transitions(transitions)
    fst.add_final_state('q1')
    return fst


def normalize_token(token: str, fst: FST) -> str:
    """
    Translates a single raw token using the specified FST.
    If no match is found, returns the upper-case version of the original token.
    """
    translations = list(fst.translate([token]))
    if translations:
        first_path = translations
        return "".join(str(symbol) for symbol in first_path)
    return token.upper()


if __name__ == "__main__":
    # Local verification tests
    fst_pl = build_programming_languages_fst()
    fst_fw = build_frameworks_fst()
    fst_db = build_databases_fst()
    print("\n--- Programming Languages ---")
    for token in ["JS", "javascript", "py", "Python", "TS", "c++"]:
        print(f"Input: '{token}' \t-> Canonical Output: '{normalize_token(token, fst_pl)}'")

    print("\n--- Frameworks / Libraries ---")
    for token in ["React.js", "ReactJS", "NodeJS", "Node.js", "Django", "Spring Boot", "REST API"]:
        print(f"Input: '{token}' \t-> Canonical Output: '{normalize_token(token, fst_fw)}'")

    print("\n--- Databases ---")
    for token in ["Postgres", "PostgreSQL", "mysql", "MongoDB", "mongo", "SQLite", "SQL"]:
        print(f"Input: '{token}' \t-> Canonical Output: '{normalize_token(token, fst_db)}'")
