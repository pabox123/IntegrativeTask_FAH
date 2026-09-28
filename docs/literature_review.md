# Literature Review: Formal Language Methods for Auditable Information Extraction and Normalization in ResumeLens

---

## 1. Introduction

Information Extraction (IE) from semi-structured natural language documents presents a fundamental challenge in computational linguistics and automated text processing. Professional résumés (curricula vitae) represent a prime example of semi-structured text: while they consistently contain predictable semantic categories—such as personal contact details, educational history, professional work experience, technical competencies, and project portfolios—the surface syntactic realization and structural layout vary substantially across candidates. The same underlying qualification or skill is frequently rendered through disparate lexical forms, acronyms, or formatting conventions (e.g., *JavaScript*, *Javascript*, and *JS*; or *Scikit-learn*, *sklearn*, and *scikit learn*).

In modern Human Resources (HR) software engineering, automated resume screening systems are tasked with ingesting these heterogeneous documents to determine whether candidate qualifications fulfill specific job profile requirements. Historically, information extraction pipelines have drifted toward purely data-driven statistical models, named entity recognition (NER) classifiers, or large language models (LLMs). Although statistical methods offer flexibility when encountering unconstrained text, they introduce non-determinism, opacity ("black-box" decisions), high computational overhead, and susceptibility to generative hallucinations.

To mitigate these limitations, the **ResumeLens** framework grounds its information processing pipeline strictly in **Formal Language Theory**. By structuring text processing across the Chomsky hierarchy—leveraging Regular Languages for extraction, Finite-State Transducers (FSTs) for normalization, Deterministic Finite Automata (DFAs) for profile pattern recognition, and Context-Free Grammars (CFGs) for structural specification—ResumeLens establishes a mathematically sound, highly performant, and fully auditable architecture.

This literature review provides the theoretical justification for employing formal methods—specifically Regular Expressions (Regex) and Finite-State Transducers (FST)—as the foundational lexical extraction and normalization stages within the ResumeLens pipeline.

---

## 2. Regular Expressions (Regex) for Lexical Analysis & Extraction

### 2.1 Theoretical Foundations

The first stage of lexical analysis in formal processing relies on the theory of **Regular Languages**. Given a finite tape alphabet $\Sigma$, the set of regular languages over $\Sigma$ is defined inductively as the smallest family of languages containing the basic regular languages:
1. The empty set $\emptyset$,
2. The empty string language $\{\lambda\}$,
3. The singleton language $\{a\}$ for every symbol $a \in \Sigma$,

and closed under the fundamental regular operations:
* **Union:** $A \cup B = \{ w \mid w \in A \lor w \in B \}$
* **Concatenation:** $A \cdot B = \{ uv \mid u \in A \land v \in B \}$
* **Kleene Closure:** $A^* = \bigcup_{i=0}^{\infty} A^i$, where $A^0 = \{\lambda\}$ and $A^{i+1} = A \cdot A^i$.

A **Regular Expression** $R$ is a formal algebraic syntax representing a regular language $L(R)$. By Kleene's Theorem, for every regular expression $R$, there exists an equivalent **Deterministic Finite Automaton (DFA)** $M = (\Sigma, Q, q_0, F, \delta)$ or **Non-deterministic Finite Automaton (NFA)** $M' = (\Sigma, Q, q_0, F, \Delta)$ such that $L(R) = L(M) = L(M')$.

A DFA is defined formally as a 5-tuple:
$$M = (\Sigma, Q, q_0, F, \delta)$$
where:
* $\Sigma$ is the finite tape input alphabet,
* $Q = \{q_0, q_1, \dots, q_n\}$ is the finite set of internal states,
* $q_0 \in Q$ is the unique initial state,
* $F \subseteq Q, F \neq \emptyset$ is the set of final or accepting states,
* $\delta: Q \times \Sigma \to Q$ is the deterministic state transition function.

Because $\delta$ is fully defined for every state-symbol pair $(q, s) \in Q \times \Sigma$, a DFA processes an input string $u \in \Sigma^*$ in linear time $O(\vert{}u\vert{})$ by reading one symbol per computational step and shifting its reading head strictly to the right across the tape cells.

### 2.2 Practical Application in ResumeLens

In the ResumeLens extraction architecture (Stage 1), regular expressions serve as deterministic lexical analyzers (tokenizers) operating directly on raw resume text $u \in \Sigma^*$. Rather than attempting to evaluate whether a candidate fulfills a profile, Stage 1 isolates candidate entity strings from surrounding prose.

1. **Contact Information & Metadata Extraction:**
    * **Email Addresses:** Formally captured via pattern matching over local and domain alphabets:  
      `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
    * **Phone Numbers & Digital Identifiers:** Matching numeric sequences with optional country codes, delimiters, and standard punctuation formats.
2. **Chronological & Quantitative Data:**
    * **Years of Experience & Dates:** Identifying duration patterns such as `\b\d{1,2}\s+(?:years?|yrs?)\b` or date ranges `(?:19|20)\d{2}` to extract temporal qualification bounds.
3. **Technical Keywords & Candidate Qualifications:**
    * Unnormalized tech tokens are extracted using bounded word boundary matchers and character classes:  
      `\b(JS|JavaScript|React\.js|NodeJS|Postgres|PostgreSQL|sklearn|Scikit-learn|Git)\b`

By compiling regular expressions into deterministic finite state machines, lexical scanning executes in $O(\vert{}u\vert{})$ worst-case time complexity, providing an efficient pattern recognition engine that extracts candidates' claimed skills without making assumptions regarding semantic equivalence or ordering.

---

## 3. Finite-State Transducers (FST) for Lexical Normalization

### 3.1 Theoretical Foundations

While finite automata (DFAs/NFAs) are language *recognizers* that output a binary accept/reject decision ($u \in L(M)$), a **Finite-State Transducer (FST)** is an automaton equipped with an output tape. FSTs compute **Regular Relations** (or rational relations) $R \subseteq \Sigma^* \times \Gamma^*$, mapping strings from an input alphabet $\Sigma$ to corresponding strings in an output alphabet $\Gamma$.

Formally, a **Deterministic Finite-State Transducer** is defined as a 7-tuple:
$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$
where:
* $Q$ is the finite set of states,
* $\Sigma$ is the finite input alphabet,
* $\Gamma$ is the finite output alphabet,
* $\delta: Q \times (\Sigma \cup \{\lambda\}) \to Q$ is the state transition function,
* $\omega: Q \times (\Sigma \cup \{\lambda\}) \to \Gamma \cup \{\lambda\}$ is the output function (emitting output symbols or strings),
* $q_0 \in Q$ is the initial start state,
* $F \subseteq Q, F \neq \emptyset$ is the set of accepting states.

Transitions in an FST transition diagram are labeled as $u : v$, where $u \in \Sigma \cup \{\lambda\}$ represents the consumed input symbol and $v \in \Gamma \cup \{\lambda\}$ represents the emitted output symbol. An input string $u \in \Sigma^*$ yields an output translation $v \in \Gamma^*$ if there exists a valid computational path from $q_0$ to some $q_f \in F$ such that the concatenation of input labels along the path equals $u$ and the concatenation of output labels equals $v$.

### 3.2 Role in Qualification Normalization for ResumeLens

In Stage 2 of ResumeLens, extracted candidate tokens suffer from typographical variations, stylistic preferences, and synonymy. To prevent downstream qualification pattern matching from failing due to superficial surface differences, an FST acts as a canonical normalizer, translating heterogeneous representations into standardized tokens:

$$T_{\text{norm}}: \text{Variant Token} \mapsto \text{Canonical Qualification Token}$$

#### Concrete Transduction Mappings:
* **JavaScript Variations:**
    * `"JS" \mapsto "JAVASCRIPT"`
    * `"Javascript" \mapsto "JAVASCRIPT"`
    * `"JavaScript" \mapsto "JAVASCRIPT"`
* **Machine Learning Library Variations:**
    * `"sklearn" \mapsto "SCIKIT_LEARN"`
    * `"scikit learn" \mapsto "SCIKIT_LEARN"`
    * `"Scikit-learn" \mapsto "SCIKIT_LEARN"`
* **Database & Tool Variations:**
    * `"Postgres" \mapsto "POSTGRESQL"`
    * `"PostgreSQL" \mapsto "POSTGRESQL"`

#### Canonical Ordering & Stream Preparation:
Following token-level transduction, normalized qualifications are sorted into a fixed canonical sequence dictated by the candidate profile definition (e.g., for a Full Stack profile: $\text{Frontend} \to \text{Backend} \to \text{Database} \to \text{Version Control}$). This ensures that subsequent classification automata process an ordered input stream $w \in \Gamma^*$, rendering qualification pattern evaluation invariant to the arbitrary ordering of skills within the raw resume.

In implementation frameworks such as `pyformlang`, FSTs are formally instantiated by adding explicit state transitions `(q_in, input_symbol, q_out, [output_symbols])`, enabling programmatic translation of token sequences via $L(T) = \{ (u, v) \mid \delta^*(q_0, u) \cap F \neq \emptyset \land v \in \omega^*(q_0, u) \}$.

---

## 4. Comparative Analysis: Formal Methods vs. Data-Driven / LLM Approaches

To evaluate why formal language models are optimal for ResumeLens, we contrast Regex/FST pipelines against statistical Machine Learning (ML), Deep Learning (DL), and Large Language Model (LLM) approaches across four critical engineering dimensions.

| Dimension | Formal Methods (Regex + FST + Automata) | Data-Driven / LLM Approaches (Transformers, Prompting) |
| :--- | :--- | :--- |
| **Explainability & Transparency** | **100% Deterministic & Traceable:** Computational steps are explicit state transitions ($q_i \xrightarrow{u:v} q_j$). Every decision can be proven via formal state traces. | **Opaque "Black Box":** Decisions stem from high-dimensional matrix multiplications and probabilistic attention weights. Internal reasoning cannot be formally proven. |
| **Determinism & Reproducibility** | **Absolute Consistency:** Identical input string $u$ strictly guarantees identical output token sequence $v$ across every execution. | **Stochastic / Variable:** Output varies based on temperature sampling, seed variations, context window shifts, or model version updates. |
| **Computational Efficiency** | **Minimal Overhead ($O(\vert{}u\vert{})$):** Executes in linear time with minimal memory footprints ($O(\vert{}Q\vert{})$ states), suitable for real-time, low-resource deployment. | **High Resource Cost ($O(N^2)$ / GPU Bound):** Requires heavy hardware acceleration, high memory consumption, and substantial inference latency. |
| **Auditing & Bias Mitigation** | **Audit-Ready & Bias-Free:** Evaluates strictly defined qualification syntax. Completely isolated from latent demographic biases or hallucinations. | **Susceptible to Bias & Hallucination:** Risk of encoding implicit societal biases from training corpora or fabricating non-existent candidate skills. |

### 4.1 Explainability and Mathematical Traceability
In HR recruitment systems, decision-making systems must explain *why* a candidate was accepted or rejected. Under a formal approach, if a resume fails screening, the system outputs the exact failing state $q_k \notin F$ and the missing symbol $s \in \Sigma$ that caused computation to abort. Conversely, deep learning models provide probabilistic confidence scores without formal structural proofs.

### 4.2 Regulatory Compliance and Anti-Discrimination Auditing
Regulatory frameworks (e.g., the EU AI Act and EEOC guidelines for automated hiring tools) strictly mandate that automated screening tools must be auditable, non-discriminatory, and free from adverse impact. Statistical models trained on historical hiring data frequently inherit implicit human biases related to gender, ethnicity, or institution names. ResumeLens avoids latent bias by restricting its analysis to explicitly specified formal qualification grammars.

---

## 5. Conclusion

The integration of Regular Expressions for information extraction and Finite-State Transducers for lexical normalization establishes a mathematically rigorous, highly efficient, and auditable foundation for the **ResumeLens** architecture.

By leveraging regular operations ($\cup, \cdot, *$) and regular relations ($R \subseteq \Sigma^* \times \Gamma^*$), ResumeLens transforms noisy, heterogeneous text into clean, canonically ordered token streams. This deterministic pre-processing stage directly enables subsequent formal validation stages:
1. **Qualification Pattern Recognition** via Deterministic Finite Automata (DFAs), and
2. **Structural Candidate Profile Specification** via Context-Free Grammars (CFGs) implemented in domain-specific language frameworks such as `textX`.

Ultimately, combining formal lexical tools ensures that candidate screening remains strictly grounded in verifiable syntactic and semantic rules—delivering high computational precision while fulfilling all transparency and compliance requirements of modern recruitment systems.

---

## References & Formal Foundations
* Chomsky, N. (1956). *Three models for the description of language*. IRE Transactions on Information Theory, 2(3), 113-124.
* Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
* Aristizábal, A. A. (2026). *Computación y Estructuras Discretas III: Slide Series on Automata Theory, Regular Languages, FSTs, and CFGs*. Departamento de Computación y Sistemas Inteligentes, Universidad ICESI.
* Pyformlang Documentation: *Formal Language Manipulation Library in Python*.