# ResumeLens: Formal Language-Based Automated Resume Screening System
**Authors:** Valeria Piza, Krystal Giraldo, Miguel Pabon
**Affiliation:** Universidad ICESI — Formal Languages and Automata Theory (2026-2)

---

## 1. Abstract
ResumeLens is an automated resume screening and candidate qualification verification system grounded strictly in Formal Language and Automata Theory . Modern recruitment pipelines frequently suffer from non-deterministic, opaque heuristics and the hallucination risks inherent to Large Language Models (LLMs). To guarantee complete transparency, deterministic reproducibility, and zero hallucination, ResumeLens implements an end-to-end processing pipeline spanning four discrete computational stages across the Chomsky hierarchy: (1) Lexical Extraction using Regular Expressions ($R$) to isolate candidate metadata and raw technical keywords; (2) Lexical Normalization and Canonical Sorting using Finite-State Transducers (FST, $M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$) to map heterogeneous surface variants (e.g., React.js, JS, k8s) into standardized canonical tokens sorted by an order-independent foundational hierarchy; (3) Profile Classification via Deterministic Finite Automata (DFA, $M = (Q, \Sigma, \delta, q_0, F)$) recognizing distinct software engineering profiles (Full Stack Developer, Machine Learning Engineer, DevOps Engineer, and NLP Engineer); and (4) Structural Specification using a Context-Free Grammar (CFG, $G = (V, \Sigma, P, S)$) implemented in Backus-Naur Form (BNF/EBNF) via textX to generate validated abstract syntax trees and export comprehensive static HTML candidate evaluation reports . Rigorous experimental verification confirms 100% test pass rates across 102 test cases, proving the efficacy of formal models in human resource automation.

---

## 2. Problem Statement & Theoretical Motivation
### The Challenge of Resume Skill Representation
In technical talent acquisition, evaluating resumes (curricula vitae) involves parsing semi-structured natural language documents exhibiting high lexical variability and arbitrary formatting:
* **Synonymy and Orthographic Variance:** The identical competency is represented through diverse aliases, such as JS, JavaScript, and javascript; React.js, ReactJS, and react; or k8s and Kubernetes .
* **Order Dependency:** Candidate resumes present technical skills in arbitrary chronological, spatial, or alphabetical orderings, requiring permutation-invariant pattern evaluation .
* **Syntactic Noise:** Contact metadata, dates of employment, and educational credentials appear interleaved with conversational prose .

### Limitations of Heuristic and LLM-Based Screening
Contemporary automated screening predominantly relies on statistical natural language processing, vector similarity embeddings, or generative Large Language Models (LLMs). While flexible, these statistical approaches introduce critical liabilities:
* **Non-Determinism and Variability:** Identical candidate resumes can yield divergent evaluation scores across executions due to probabilistic sampling and context fluctuations .
* **Generative Hallucination:** Generative architectures risk fabricating credentials or falsely attributing unverified skills to candidates .
* **Opaque "Black-Box" Decisions:** Neural network attention matrices cannot provide formal, auditable verification traces required by regulatory recruitment compliance (e.g., EU AI Act, EEOC anti-discrimination standards) .

### The Formal Language Paradigm
By mapping resume screening directly onto formal computational models—Regular Expressions, Finite-State Transducers, Deterministic Finite Automata, and Context-Free Grammars—ResumeLens establishes:
1. **Mathematical Determinism:** Every state transition $q_i \xrightarrow{\sigma} q_j$ is uniquely defined and fully reproducible .
2. **Auditable Proof Traces:** Rejections specify the exact non-accepting state and missing canonical skill symbol .
3. **Computational Efficiency:** Linear-time recognition complexity $\mathcal{O}(|u|)$, eliminating GPU dependencies and high operational inference costs .
4. **Zero Hallucination:** Strict boundary enforcement prevents attributing any qualification not explicitly present in the input text .

---

## 3. System Architecture & Formal Methodology
ResumeLens processes raw candidate resumes through a sequential 4-stage pipeline :

```text
[Raw Resume Text]
│
▼
┌────────────────────────────────────────────────────────┐
│ Stage 1: Lexical Extraction (Regular Expressions)     │
│ - ContactExtractor, LanguageExtractor, Frameworks, etc.│
└────────────────────────────────────────────────────────┘
│ Extracted Substrings & Raw Tokens
▼
┌────────────────────────────────────────────────────────┐
│ Stage 2: Normalization & Canonical Sorting (FST)       │
│ - Category FSTs (pyformlang) : Raw Token ↦ Canonical   │
│ - Hierarchical Canonical Rank Sort (Order Independence)│
└────────────────────────────────────────────────────────┘
│ Canonical Ordered Token Sequence w ∈ Σ*
▼
┌────────────────────────────────────────────────────────┐
│ Stage 3: Profile Classification (DFA Automata)        │
│ - Full Stack, ML Engineer, DevOps, NLP Engineer DFAs   │
│ - Deterministic Decision: ACCEPTED / REJECTED          │
└────────────────────────────────────────────────────────┘
│ Candidate Metadata + Skills + Evaluation
▼
┌────────────────────────────────────────────────────────┐
│ Stage 4: DSL Specification & Visualization (CFG/EBNF)  │
│ - textX Grammar Metamodel (AST Validation)             │
│ - Static HTML Report Generation                        │
└────────────────────────────────────────────────────────┘
```

---

### Stage 1: Lexical Extraction (Regex)
**Theoretical Definition:**
Given an input character alphabet $\Sigma$ (ASCII/Unicode character sets), a regular expression $R$ over $\Sigma$ denotes a regular language $L(R) \subseteq \Sigma^*$ defined inductively through the base elements $\emptyset, \varepsilon, a \in \Sigma$ and the regular operations :
* **Union:** $(r_1 \mid r_2)$
* **Concatenation:** $(r_1 \cdot r_2)$
* **Kleene Star:** $(r_1^*)$

**Implementation in ResumeLens:**
Stage 1 deploys modular extractors orchestrated by the unified ResumeExtractor facade :
* **ContactExtractor:**
    * *Email:* `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b`
    * *Phone:* `\b(?:\+?\d{1,3}[-.\s]?)?$?\d{3}$?[-.\s]?\d{3}[-.\s]?\d{4}\b`
    * *LinkedIn:* `\b(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+\/?\b`
* **LanguageExtractor:** Matches foundational programming languages using word boundaries (`\b`), preventing sub-token collisions (e.g., Python3?, Java, JavaScript|JS, TypeScript|TS, C++, SQL, R) .
* **FrameworkExtractor:** Captures frontend libraries (React(.js)?, Vue(.js)?, Angular), backend frameworks (Node(.js)?, Express(.js)?, Django, Spring(\s*Boot)?), and machine learning libraries (Pandas, NumPy, Scikit-learn|sklearn, TensorFlow, PyTorch) .
* **DatabaseToolExtractor:** Extracts database engines (PostgreSQL|Postgres, MySQL, MongoDB, Redis) and infrastructure tools (Docker, Kubernetes|k8s, Git, Jenkins, Terraform, AWS, GCP, Azure) .
* **EducationExtractor & ExperienceExtractor:** Isolates academic credentials (Bachelor, Master, Ph.D., B.Sc.) and tenure durations (`\d+(?:\.\d+)?\s+(?:years?|months?)`) .

---

### Stage 2: Skill Normalization & Canonical Sorting (FST)
**Theoretical Definition:**
A Finite-State Transducer (FST) is formally defined as a 7-tuple :


M = (Q, Σ, Γ, δ, ω, q₀, F)


where:
* $Q$ is the finite, non-empty set of internal states .
* $\Sigma$ is the finite input alphabet (raw extracted tokens) .
* $\Gamma$ is the finite output alphabet (standardized canonical symbols) .
* $\delta: Q \times \Sigma \to Q$ is the state transition function .
* $\omega: Q \times \Sigma \to \Gamma^*$ is the output translation function (Mealy transducer model) .
* $q_0 \in Q$ is the unique initial state .
* $F \subseteq Q$ is the set of final/accepting states .

#### Concrete Formal Specification for Programming Language Normalization ($M_{\text{PL}}$):
For normalizing surface variations of JavaScript (including "JS" $\mapsto$ "JAVASCRIPT"), Python, TypeScript, Java, and C++, the transducer $M_{\text{PL}} = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$ is concretely instantiated as :
* **States:** $Q = \{q_0, q_1\}$
* **Input Alphabet:** $\Sigma = \{\text{"JS"}, \text{"js"}, \text{"Js"}, \text{"JavaScript"}, \text{"javascript"}, \text{"JAVASCRIPT"}, \text{"py"}, \text{"Python"}, \text{"TS"}, \text{"TypeScript"}, \text{"Java"}, \text{"C++"}, \dots\}$
* **Output Alphabet:** $\Gamma = \{\text{"JAVASCRIPT"}, \text{"PYTHON"}, \text{"TYPESCRIPT"}, \text{"JAVA"}, \text{"CPP"}, \dots\}$
* **Initial State:** $q_0 = q_0$
* **Accepting States:** $F = \{q_1\}$
* **Transition ($\delta$) and Output ($\omega$) Functions (Mealy Transitions):**
  

δ(q₀, "JS") = q₁,  ω(q₀, "JS") = "JAVASCRIPT"


  

δ(q₀, "js") = q₁,  ω(q₀, "js") = "JAVASCRIPT"


  

δ(q₀, "JavaScript") = q₁,  ω(q₀, "JavaScript") = "JAVASCRIPT"


  

δ(q₀, "py") = q₁,  ω(q₀, "py") = "PYTHON"


  

δ(q₀, "React.js") = q₁,  ω(q₀, "React.js") = "REACT" (via M_FW)


  

δ(q₀, "k8s") = q₁,  ω(q₀, "k8s") = "KUBERNETES" (via M_DO)



Formally, the rational relation realized by $M_{\text{PL}}$ accepts the pair $(\text{"JS"}, \text{"JAVASCRIPT"})$ because :


δ*(q₀, "JS") = q₁ ∈ F and ω*(q₀, "JS") = "JAVASCRIPT"



**Hierarchical Canonical Sorting Algorithm:**
Raw resumes present skills in non-deterministic permutations . To ensure deterministic sequential evaluation by downstream automata, the SkillNormalizerPipeline maps canonical tokens to a foundational rank hierarchy $\mathcal{H}$ :


Rank: Programming Languages [10–19] ≺ Frontend [20–29] ≺ Backend [30–39] ≺ Databases [40–49] ≺ DevOps [50–59] ≺ AI/ML [60–69]





CANONICAL_RANK: {JAVASCRIPT: 10, TYPESCRIPT: 11, PYTHON: 12, REACT: 20, NODE_JS: 30, POSTGRESQL: 40, GIT: 52, …}



Given an unordered set of extracted tokens $S = \{\text{"Git"}, \text{"NodeJS"}, \text{"JS"}, \text{"Postgres"}, \text{"React.js"}\}$, the pipeline normalizes and canonically sorts the elements into an invariant sequence :


w = ⟨JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT⟩



---

### Stage 3: Profile Classification (DFA Automata)
**Theoretical Definition:**
A Deterministic Finite Automaton (DFA) is formally defined as a 5-tuple :


M = (Q, \Sigma, \delta, q_0, F)


where:
* $Q$ is the finite set of internal control states .
* $\Sigma$ is the input alphabet consisting strictly of canonical qualification tokens .
* $\delta: Q \times \Sigma \to Q$ is the deterministic transition function satisfying $|\delta(q, \sigma)| = 1$ for all $(q, \sigma) \in Q \times \Sigma$ .
* $q_0 \in Q$ is the designated start state .
* $F \subseteq Q$ is the non-empty set of accepting final states .

A normalized sequence $w = \sigma_1 \sigma_2 \dots \sigma_m \in \Sigma^*$ is accepted if and only if $\delta^*(q_0, w) \in F$ .

#### Full Stack Developer DFA Formalization (full_stack_dfa.py):
* **States:** $Q = \{q_0, q_1, q_2, q_3, q_4, q_{\text{reject}}\}$ 
* **Initial State:** $q_0$ 
* **Accepting States:** $F = \{q_4\}$ 
* **Canonical Input Alphabet ($\Sigma_{\text{FS}}$):** 


($\Sigma_{\text{FS}} = \Sigma_{\text{Front}} \cup \Sigma_{\text{Back}} \cup \Sigma_{\text{DB}} \cup \Sigma_{\text{VC}} \cup \{\text{OTHER}\}$)


  where:<br>
    $\Sigma_{\text{Front}} = \{\text{JAVASCRIPT}, \text{TYPESCRIPT}, \text{REACT}, \text{ANGULAR}, \text{VUE}\}$<br>
    $\Sigma_{\text{Back}} = \{\text{NODE_JS}, \text{DJANGO}, \text{SPRING_BOOT}, \text{EXPRESS}\}$<br>
    $\Sigma_{\text{DB}} = \{\text{POSTGRESQL}, \text{MYSQL}, \text{MONGODB}, \text{SQL}, \text{NOSQL}\}$<br>
    $\Sigma_{\text{VC}} = \{\text{GIT}\}$<br>
    $\text{OTHER} = \text{Any canonical symbol } \sigma \notin \Sigma_{\text{FS}}$

#### Transition Function Table $\delta(q, \sigma)$ for Full Stack Developer:
| Current State $q$ | Input Symbol $\sigma \in \Sigma_{\text{Front}}$ | Input Symbol $\sigma \in \Sigma_{\text{Back}}$ | Input Symbol $\sigma \in \Sigma_{\text{DB}}$ | Input Symbol $\sigma \in \Sigma_{\text{VC}}$ | Symbol $\sigma = \text{OTHER}$ | State Semantics / Qualification Level |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **$q_0$** | **$q_1$** | $q_{\text{reject}}$ | $q_{\text{reject}}$ | $q_{\text{reject}}$ | $q_{\text{reject}}$ | Initial state: awaiting Frontend competence  |
| **$q_1$** | $q_1$ | **$q_2$** | $q_{\text{reject}}$ | $q_{\text{reject}}$ | $q_{\text{reject}}$ | Frontend verified; awaiting Backend  |
| **$q_2$** | $q_1$ | $q_2$ | **$q_3$** | $q_{\text{reject}}$ | $q_{\text{reject}}$ | Backend verified; awaiting Database  |
| **$q_3$** | $q_1$ | $q_2$ | $q_3$ | **$q_4$** | $q_{\text{reject}}$ | Database verified; awaiting Version Control  |
| **$q_4$ (Accept)** | $q_4$ | $q_4$ | $q_4$ | $q_4$ | $q_{\text{reject}}$ | **Accepted:** Full Stack pattern satisfied  |
| **$q_{\text{reject}}$** | $q_{\text{reject}}$ | $q_{\text{reject}}$ | $q_{\text{reject}}$ | $q_{\text{reject}}$ | $q_{\text{reject}}$ | **Dead/Trap state:** Missing requisite category  |

#### Additional Implemented Engineering Profile DFAs:
1. **Machine Learning Engineer DFA (ml_engineer_dfa.py):** 
    * $Q = \{q_0, \dots, q_6, q_{\text{reject}}\}, F = \{q_6\}$.
    * Canonical Path: $\text{Languages } (\text{PYTHON, R}) \to \text{Data Processing } (\text{PANDAS, NUMPY}) \to \text{ML Libraries } (\text{SCIKIT\_LEARN, XGBOOST}) \to \text{Deep Learning } (\text{TENSORFLOW, PYTORCH}) \to \text{Databases } (\text{SQL, POSTGRESQL, MYSQL, BIGQUERY}) \to \text{Version Control } (\text{GIT})$.
2. **DevOps Engineer DFA (devops_dfa.py):** 
    * $Q = \{q_0, \dots, q_7, q_{\text{reject}}\}, F = \{q_7\}$.
    * Canonical Path: $\text{Scripting } (\text{PYTHON, BASH, POWERSHELL}) \to \text{Containers } (\text{DOCKER, KUBERNETES, HELM}) \to \text{CI/CD } (\text{JENKINS, GITLAB\_CI, GITHUB\_ACTIONS}) \to \text{IaC } (\text{TERRAFORM, ANSIBLE, CLOUDFORMATION}) \to \text{Cloud } (\text{AWS, AZURE, GCP}) \to \text{Monitoring } (\text{PROMETHEUS, GRAFANA, ELK}) \to \text{Version Control } (\text{GIT})$.
3. **NLP Engineer DFA (nlp_engineer_dfa.py):** 
    * $Q = \{q_0, \dots, q_6, q_{\text{reject}}\}, F = \{q_6\}$.
    * Canonical Path: $\text{Languages } (\text{PYTHON, SQL, BASH}) \to \text{NLP Libraries } (\text{SPACY, NLTK, GENSIM}) \to \text{Deep Learning } (\text{PYTORCH, TENSORFLOW, TRANSFORMERS}) \to \text{Pretrained Models } (\text{BERT, ROBERTA}) \to \text{Databases } (\text{POSTGRESQL, MYSQL, ELASTICSEARCH}) \to \text{Tools } (\text{DOCKER, GIT, JUPYTER, FASTAPI})$.

---

### Stage 4: Domain-Specific Language & Visualization (CFG & EBNF)
**Theoretical Definition:**
A Context-Free Grammar (CFG) is formally defined as a 4-tuple :


G = (V, \Sigma, P, S)


where:
* $V$ is a finite set of non-terminal syntactic variables :
  

V = $\{\text{CandidateProfile}, \text{Experience}, \text{SkillEntry}, \text{SkillToken}, \text{Evaluation}\}$


* $\Sigma$ is a finite set of terminal symbols disjoint from $V$ :
  

$\Sigma = \{\text{'CandidateProfile'}, \text{'Experience'}, \text{'Skill'}, \text{'Evaluation'}, \text{'{'}, \text{'}'}, \text{':'}, \text{'name'}, \text{'email'}, \text{'location'}, \text{'current\_role'}, \text{'summary'}, \text{'company'}, \text{'duration'}, \text{'description'}, \text{'profile'}, \text{'result'}, \text{STRING}, \text{ID}, \text{SkillTokenRegex}\}$


* $S \in V$ is the start symbol ($S = \text{CandidateProfile}$) .
* $P$ is the finite set of context-free production rules specified below .

#### Formal Production Rules $P$ (EBNF Metamodel in textX — resume_dsl.tx):

```text
P = {
  1. CandidateProfile → 'CandidateProfile' '{'
       [ 'name' ':' STRING ]
       [ 'email' ':' STRING ]
       [ 'location' ':' STRING ]
       [ 'current_role' ':' STRING ]
       [ 'summary' ':' STRING ]
       Experience*
       SkillEntry*
       [ Evaluation ]
       '}'

  2. Experience → 'Experience' '{'
       'company' ':' STRING
       'duration' ':' STRING
       'description' ':' STRING
       '}'

  3. SkillEntry → 'Skill' ':' SkillToken

  4. SkillToken → REGEX(/[^\n]+/)

  5. Evaluation → 'Evaluation' '{'
       'profile' ':' STRING
       'result' ':' ID
       [ 'description' ':' STRING ]
       '}'
}
```
   

 

**Concrete Grammar Specification (resume_dsl.tx):**
```text
CandidateProfile:  
    'CandidateProfile' '{'  
        ('name' ':' name=STRING)?  
        ('email' ':' email=STRING)?  
        ('location' ':' location=STRING)?  
        ('current_role' ':' current_role=STRING)?  
        ('summary' ':' summary=STRING)?  
        experiences*=Experience  
        skills*=SkillEntry  
        evaluation=Evaluation?  
    '}'  
;  

Experience:  
    'Experience' '{'  
        'company' ':' company=STRING  
        'duration' ':' duration=STRING  
        'description' ':' description=STRING  
    '}'  
;  

SkillEntry:  
    'Skill' ':' value=SkillToken  
;  

SkillToken:  
    /[^\n]+/  
;  

Evaluation:  
    'Evaluation' '{'  
        'profile' ':' profile=STRING  
        'result' ':' result=ID  
        ('description' ':' description=STRING)?  
    '}'  
;
``` 

**AST Parsing & Visualization:**
1. **ResumeParser & ProfileValidator:** Parses candidate documents into an Abstract Syntax Tree (AST) rooted at $S$, validating email formatting, token capitalization, and consistency between claimed skills and the automaton's ACCEPTED/REJECTED decision .
2. **html_generator.py:** Renders the validated AST into a responsive static HTML report displaying candidate profile metadata, badge-styled canonical skills, and verification status .

---

## 4. Experimental Results, Verification & Case Studies
### Test Suite Execution Summary
The ResumeLens pipeline was rigorously tested across all four stages using pytest. The automated test suite executes **102 test cases** with a 100% pass rate :

| Test Module | Scope & Covered Functionality | Test Cases | Result |
| ------ | ------ | ------ | ------ |
| tests/test_extraction.py | Regex lexical analysis, contacts, noise robustness, case casing | 8 | **100% PASSED**  |
| tests/test_normalization.py | Category FST transducers, canonical rank sorting, interface mappings | 7 | **100% PASSED**  |
| tests/test_automata.py | Full Stack, ML, DevOps, and NLP DFAs, cross-profile exclusivity | 63 | **100% PASSED**  |
| tests/test_dsl.py | textX BNF/EBNF parsing, AST structure, ProfileValidator checks | 18 | **100% PASSED**  |
| tests/test_integration.py | End-to-end multi-stage pipeline, file-to-report consistency | 6 | **100% PASSED**  |
| **Total** | **Full System Formal Language Pipeline** | **102** | **100% PASSED**  |

*Execution Benchmark:* **102 passed in 0.72 seconds**, establishing high-throughput sub-millisecond evaluation efficiency .

### Benchmark Resume Classification
| Resume Sample | Target Engineering Profile | Automata Verdict | Pipeline Decision |
| --- | --- | --- | --- |
| cv_fullstack.txt | Full Stack Developer | ACCEPTED (q4) | VALID PROFILE |
| cv_ml.txt | Machine Learning Engineer | ACCEPTED (q6) | VALID PROFILE |
| cv_devops.txt | DevOps Engineer | ACCEPTED (q7) | VALID PROFILE |
| cv_nlp.txt | NLP Engineer | ACCEPTED (q6) | VALID PROFILE |
| Unqualified CV | Unqualified Candidate | REJECTED (q_reject) | UNKNOWN PROFILE |

---

### Case Study: Transformation Trace for 'Wednesday Addams'
To demonstrate complete end-to-end formal trace execution, we examine the transformation of candidate **Wednesday Addams** (samples/candidates/wednesday_addams.resume) :

#### 1. Input Resume Representation:
Candidate claims web application experience, personal contacts (wednesday.addams@example.com), and four technical skills: JavaScript, React, PostgreSQL, and Git .

#### 2. Stage 1 — Lexical Extraction:
The regular expression extractors isolate :
* Personal Data: $\text{Email} = \text{"wednesday.addams@example.com"}$
* Extracted Raw Tokens: $S_{\text{raw}} = \{\text{"JavaScript"}, \text{"React"}, \text{"PostgreSQL"}, \text{"Git"}\}$
* Tenure Duration: $\text{"3 years"}$

#### 3. Stage 2 — FST Normalization & Canonical Sorting:

Each raw token is transduced via `M_PL`, `M_FW`, `M_DB`, `M_DO`:

```text
ω*(q₀, "JavaScript") = "JAVASCRIPT"

ω*(q₀, "React") = "REACT"

ω*(q₀, "PostgreSQL") = "POSTGRESQL"

ω*(q₀, "Git") = "GIT"
```

Applying the canonical rank hierarchy (`JAVASCRIPT: 10 ≺ REACT: 20 ≺ POSTGRESQL: 40 ≺ GIT: 52`):

```text
w_Wednesday = ⟨JAVASCRIPT, REACT, POSTGRESQL, GIT⟩
```

#### 4. Stage 3 — DFA Profile Evaluation Trace:

Feeding the sequence `w_Wednesday` into the Full Stack Developer DFA (`M_FS`):

```text
δ(q₀, JAVASCRIPT) = q₁  (Frontend Seen)

δ(q₁, REACT) = q₁  (Frontend Self-loop)

δ(q₁, POSTGRESQL) = q_reject  (**Rejection: Missing Backend Qualification**)

δ(q_reject, GIT) = q_reject  (Rejection: Incompatible with Rejected State)
```

Since `δ*(q₀, w_Wednesday) = q_reject ∉ F`, the automaton **REJECTS** the profile. The candidate lacks a required backend competency (`NODE_JS`, `DJANGO`, `SPRING_BOOT`, `EXPRESS`).
#### 5. Stage 4 — DSL AST Generation & Evaluation Output:
The system derives a valid DSL document belonging to $L(G)$ :
```text
CandidateProfile {  
    name: "Wednesday Addams"  
    email: "wednesday.addams@example.com"  
    location: "Nevermore Academy, Jericho"  
    current_role: "Unknown"  
    summary: "Candidate profile generated by ResumeLens"  
    Experience {  
        company: "Nevermore Academy Projects"  
        duration: "3 years"  
        description: "Developed web applications"  
    }  
    Skill: JAVASCRIPT  
    Skill: REACT  
    Skill: POSTGRESQL  
    Skill: GIT  
    Evaluation {  
        profile: "Unknown"  
        result: REJECTED  
        description: "The normalized qualifications do not satisfy any accepted profile pattern."  
    }  
}
``` 

**Conclusion:** The mathematical trace provides an indisputable, auditable reason for rejection: failure to transition from state $q_1$ to $q_2$ due to an empty backend alphabet intersection .

---

## 5. Conclusions & Advantages
ResumeLens demonstrates that classical **Formal Language and Automata Theory** offers an effective, transparent, and superior alternative to heuristic and generative approaches for automated candidate screening :
1. **Mathematical Determinism & Zero Hallucination:** Every screening outcome is guaranteed by explicit transition functions ($\delta, \omega$). The system never fabricates skills or produces probabilistic discrepancies .
2. **End-to-End Auditing & Regulatory Compliance:** Each decision yields a deterministic execution path. If a candidate is rejected, the system identifies the exact missing canonical symbol and final non-accepting state, satisfying transparency mandates under automated employment decision laws .
3. **High Computational Efficiency:** Operating in linear time $\mathcal{O}(|u|)$, the pipeline processes resumes in milliseconds on standard CPU hardware without GPU acceleration or cloud inference APIs .
4. **Modularity Across the Chomsky Hierarchy:** Decoupling lexical extraction (Regex), normalization (FST), pattern recognition (DFA), and document specification (CFG/DSL) creates an easily extensible architecture for adding new technical profiles .

---

## References
1. Chomsky, N. (1956). *Three models for the description of language*. IRE Transactions on Information Theory, 2(3), 113–124 .
2. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley .
3. Aristizábal, A. A. (2026). *Computación y Estructuras Discretas III: Lecture Notes on Automata Theory, FSTs, and Formal Grammars*. Universidad ICESI .
4. De la Higuera, C. (2010). *Grammatical Inference: Learning Automata and Grammars*. Cambridge University Press .
5. pyformlang & textX Documentation (2026). *Formal Language Manipulation and Domain-Specific Language Metamodeling in Python* .
