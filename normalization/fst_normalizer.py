from pyformlang.fst import FST


def build_programming_languages_fst() -> FST:
    """
    Constructs a Finite-State Transducer (FST) for normalizing programming language tokens.

    Formal Definition (7-tuple): M = (Q, Σ, Γ, δ, ω, q0, F)
    - Q: {'q0', 'q1'}
    - Σ: Raw input tokens ('JS', 'js', 'py', 'Python', 'TS', 'c++', etc.)
    - Γ: Canonical output tokens ('JAVASCRIPT', 'PYTHON', 'TYPESCRIPT', 'CPP', etc.)
    - δ: Transition function between states
    - ω: Output mapping function
    - q0: Start state 'q0'
    - F: Final accepting states {'q1'}
    """
    fst = FST()

    # Define start state
    fst.add_start_state('q0')

    # Transitions format: (state_from, input_symbol, state_to, [output_symbol])
    transitions = [
        # JavaScript variants -> JAVASCRIPT
        ('q0', 'JS', 'q1', ['JAVASCRIPT']),
        ('q0', 'js', 'q1', ['JAVASCRIPT']),
        ('q0', 'Js', 'q1', ['JAVASCRIPT']),
        ('q0', 'JavaScript', 'q1', ['JAVASCRIPT']),
        ('q0', 'javascript', 'q1', ['JAVASCRIPT']),
        ('q0', 'JAVASCRIPT', 'q1', ['JAVASCRIPT']),

        # Python variants -> PYTHON
        ('q0', 'py', 'q1', ['PYTHON']),
        ('q0', 'Py', 'q1', ['PYTHON']),
        ('q0', 'Python', 'q1', ['PYTHON']),
        ('q0', 'python', 'q1', ['PYTHON']),
        ('q0', 'PYTHON', 'q1', ['PYTHON']),

        # TypeScript variants -> TYPESCRIPT
        ('q0', 'TS', 'q1', ['TYPESCRIPT']),
        ('q0', 'ts', 'q1', ['TYPESCRIPT']),
        ('q0', 'TypeScript', 'q1', ['TYPESCRIPT']),
        ('q0', 'typescript', 'q1', ['TYPESCRIPT']),
        ('q0', 'TYPESCRIPT', 'q1', ['TYPESCRIPT']),

        # Java variants -> JAVA
        ('q0', 'Java', 'q1', ['JAVA']),
        ('q0', 'java', 'q1', ['JAVA']),
        ('q0', 'JAVA', 'q1', ['JAVA']),

        # C++ variants -> CPP
        ('q0', 'C++', 'q1', ['CPP']),
        ('q0', 'c++', 'q1', ['CPP']),
        ('q0', 'CPP', 'q1', ['CPP']),
    ]

    fst.add_transitions(transitions)
    fst.add_final_state('q1')

    return fst


def normalize_programming_language(token: str, fst: FST = None) -> str:
    """
    Translates a single raw programming language token into its canonical form.
    If no FST match is found, returns the upper-case version of the original token.
    """
    if fst is None:
        fst = build_programming_languages_fst()

    # Process translation through PyFormLang FST
    translations = list(fst.translate([token]))
    if translations:
        # PyFormLang returns a list of symbol sequences
        first_path = translations[0]
        return "".join(str(symbol) for symbol in first_path)

    return token.upper()

# Local verification test
"""
if __name__ == "__main__":
    
    fst_pl = build_programming_languages_fst()
    test_tokens = ["JS", "javascript", "py", "Python", "TS", "c++", "Java"]

    print("ResumeLens: Programming Languages FST Verification")
    for token in test_tokens:
        result = normalize_programming_language(token, fst_pl)
        print(f"Input: '{token}' \t-> Canonical Output: '{result}'")
"""