# Formalization

## ResumeLens — Formal Language-Based Resume Screening

This document establishes the base formal definitions used throughout the
ResumeLens pipeline. Each stage of the system (extraction, normalization,
pattern recognition, and structural validation) is grounded in a specific
formal language model. This document defines the general mathematical
framework for each model; the concrete instances (regular expressions per
field, transducers per qualification, automata per professional profile,
and the grammar for the candidate-profile DSL) are developed in the
subsequent design documents, once the profile-specific data is fixed.

---

## 1. Preliminaries

**Alphabet.** An alphabet $\Sigma$ is a finite, non-empty set of symbols.

**String.** A string over $\Sigma$ is a finite sequence of symbols from
$\Sigma$, including the empty string $\varepsilon$. $\Sigma^{*}$ denotes
the set of all strings over $\Sigma$, and $\Sigma^{+} = \Sigma^{*} \setminus \{\varepsilon\}$.

**Formal language.** A formal language $L$ over $\Sigma$ is any subset
$L \subseteq \Sigma^{*}$.

In ResumeLens, $\Sigma$ varies by stage: at the extraction stage it is the
character set of the raw résumé text (letters, digits, punctuation); at
the normalization and pattern-recognition stages it is the set of
qualification tokens (e.g. individual technology names) rather than raw
characters, since by that point the pipeline reasons over tokens, not
characters.

---

## 2. Regular Expressions (Stage 1 — Extraction)

A regular expression over an alphabet $\Sigma$ is defined inductively:

- $\emptyset$, $\varepsilon$, and each $a \in \Sigma$ are regular expressions.
- If $r$ and $s$ are regular expressions, then so are:
  - $(r \mid s)$ — union,
  - $(r \cdot s)$ — concatenation,
  - $(r^{*})$ — Kleene star.

Every regular expression $r$ denotes a language $L(r) \subseteq \Sigma^{*}$,
defined by the usual structural rules. A regular expression is used at
this stage as a **recognizer/extractor**: given a résumé represented as a
string, it identifies the substrings that belong to $L(r)$ for a given
information category (e.g. contact information, programming languages,
academic degrees).

For each category of information ResumeLens extracts (contact data,
programming languages, frameworks/libraries, databases, academic
qualifications, professional experience, tools), the design documents
must state, for its corresponding expression $r$:

1. The informal textual pattern it captures.
2. The formal expression $r$ over the relevant alphabet.
3. A short justification of $L(r)$ (what strings it accepts and rejects).
4. Its Python `re` implementation.

---

## 3. Finite-State Transducers (Stage 2 — Normalization)

A finite-state transducer is formally defined as the 7-tuple:

$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$

where:

- $Q$ — a finite, non-empty set of **states**.
- $\Sigma$ — the finite **input alphabet** (tokens as extracted in Stage 1).
- $\Gamma$ — the finite **output alphabet** (canonical qualification tokens).
- $\delta: Q \times \Sigma \rightarrow Q$ — the **transition function**
  (or relation, if the transducer is non-deterministic), mapping a state
  and an input symbol to a next state.
- $\omega: Q \times \Sigma \rightarrow \Gamma^{*}$ — the **output function**,
  producing an output string associated with each transition (Mealy-style)
  or with each state (Moore-style) — the design documents must state which
  convention is adopted and keep it consistent across all transducers.
- $q_0 \in Q$ — the **initial state**.
- $F \subseteq Q$ — the set of **accepting states**.

Each transducer defined for ResumeLens takes a raw qualification token
(e.g. `JS`, `Javascript`, `React.js`) as input and produces its canonical
form (e.g. `JAVASCRIPT`, `REACT`) as output, resolving the many-to-one
relationship between surface forms and canonical qualifications described
in the project brief.

For each transducer, the design documents must provide:

1. The complete 7-tuple $(Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$.
2. A graphical transition diagram.
3. Its implementation with `pyformlang`.

---

## 4. Finite Automata (Stage 3 — Pattern Recognition)

A finite automaton is formally defined as the 5-tuple:

$$M = (Q, \Sigma, \delta, q_0, F)$$

where:

- $Q$ — a finite, non-empty set of **states**.
- $\Sigma$ — the finite **input alphabet**, here the set of canonical
  qualification tokens produced by Stage 2.
- $\delta$ — the **transition function/relation**:
  - $\delta: Q \times \Sigma \rightarrow Q$ for a **DFA**,
  - $\delta: Q \times \Sigma \rightarrow \mathcal{P}(Q)$ for an **NFA**,
  - $\delta: Q \times (\Sigma \cup \{\varepsilon\}) \rightarrow \mathcal{P}(Q)$
    for an **ε-NFA**.
- $q_0 \in Q$ — the **initial state**.
- $F \subseteq Q$ — the set of **accepting states**.

A resumes normalized and sorted qualification sequence (per the canonical
order established for a given professional profile) is accepted by a
profile's automaton if and only if the sequence, read as a string over
$\Sigma$, drives the automaton from $q_0$ to a state in $F$. Each
professional profile (Full Stack Developer, Machine Learning Engineer,
and the two additional profiles chosen by the team) is modeled by its own
automaton over the corresponding qualification alphabet.

For each automaton, the design documents must provide:

1. The complete 5-tuple $(Q, \Sigma, \delta, q_0, F)$.
2. The automaton type (DFA, NFA, or ε-NFA), justified from the definition
   of $\delta$ actually used.
3. A transition diagram.
4. An explanation of the profile pattern the automaton represents.
5. Its implementation with `pyformlang`.

---

## 5. Context-Free Grammar (Stage 4 — Candidate Profile DSL)

A context-free grammar is formally defined as the 4-tuple:

$$G = (N, \Sigma, P, S)$$

where:

- $N$ — a finite set of **non-terminal symbols**.
- $\Sigma$ — a finite set of **terminal symbols**, with $N \cap \Sigma = \emptyset$.
- $P$ — a finite set of **production rules** of the form $A \rightarrow \alpha$,
  with $A \in N$ and $\alpha \in (N \cup \Sigma)^{*}$.
- $S \in N$ — the **start symbol**.

The language generated by $G$ is:

$$L(G) = \{ w \in \Sigma^{*} \mid S \Rightarrow^{*} w \}$$

Unlike Stages 1–3, this grammar does not extract, normalize, or classify
qualifications — it defines the **structural, textual language** in which
a fully processed candidate profile (personal information, contact data,
experience, skills, and profile-classification results) must be written
to be considered a well-formed candidate-profile document. The grammar
will be specified in EBNF, identifying terminals and non-terminals, and
implemented as a metamodel with `textX`, supporting repeated structures
(multiple experiences, education records, or skills) as required by the
brief.

---

## 6. Traceability of Formal Models to Pipeline Stages

| Stage | Formal model | Input | Output |
|---|---|---|---|
| 1. Extraction | Regular expressions | Raw résumé text | Extracted qualification/contact strings |
| 2. Normalization | Finite-state transducers | Extracted strings | Canonical qualification tokens |
| 3. Pattern recognition | Finite automata (DFA/NFA/ε-NFA) | Sorted canonical tokens | ACCEPTED / REJECTED per profile |
| 4. Structural validation | Context-free grammar (textX DSL) | Structured candidate data | Valid/invalid candidate-profile document |

---

