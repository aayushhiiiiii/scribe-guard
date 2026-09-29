# Literature Notes

Reading method: three-pass (Keshav, "How to Read a Paper").
Pass 1 = 5–10 min skim. Pass 2 = ~1 hr, figures and methods, skip proofs/derivations.
Pass 3 only for papers I'm directly reimplementing.

---

## ACI-BENCH (Yim et al., Scientific Data, 2023)

**Link:** https://www.nature.com/articles/s41597-023-02487-3 (also PMC10482860)
**Code:** https://github.com/wyim/aci-bench
**Status:** Pass 2 complete

### Pass 1: Five Cs

- **Category:** Dataset / benchmark paper (a "Data Descriptor" in Scientific Data). It
  introduces data and baseline results, not a new model.
- **Context:** Clinic conversations are rarely recorded and hard to share because of
  patient privacy. Before this, public dialogue-to-note datasets were either
  snippet-level (MTS-Dialog, ~1,700 dialogue snippets) or small (PriMock57, 57 full
  encounters).
- **Correctness (first impression):** Data creation and cleaning are carefully
  documented, with medical annotators and agreement statistics. Weaker points: the
  data is synthetic and from a single institution, the realism comparison uses only
  20 encounters against a proprietary dataset, and the evaluation relies on
  word-overlap metrics that don't measure clinical correctness.
- **Contributions:** (1) The largest public corpus of full doctor-patient
  conversations paired with clinical notes, in three workflow subsets; (2) multiple
  transcript versions (human, ASR, ASR-corrected) for studying speech recognition
  effects; (3) a four-division note structure for generation and evaluation;
  (4) baseline results for many model types; (5) public data and code.
- **Clarity:** Clearly organized; some typos. The tables must be viewed directly for
  split sizes and detailed results.

### One-sentence summary

ACI-BENCH introduces the largest public dataset of full doctor-patient conversations
paired with clinical notes, spanning three note-generation workflows, and benchmarks
common summarization models on it, showing that fine-tuned models and GPT-4 perform
best but that standard automatic metrics poorly capture clinical accuracy.

### Problem

Automatic clinical note generation from visit conversations (the technology behind
ambient scribes) could reduce physicians' documentation burden, but there was no
sufficiently large, shareable dataset to benchmark and compare methods publicly.

### Method

**Data creation.** Three subsets representing different note-generation workflows:

- **virtassist:** doctor uses voice commands to a virtual assistant ("Hey Dragon...").
  Human transcription.
- **virtscribe:** doctor gives a pre-visit intro and post-visit dictation to a scribe.
  Human transcription + ASR versions.
- **aci:** natural conversation with no commands (closest to modern ambient scribes).
  ASR + human-corrected ASR versions.

virtassist/virtscribe transcripts were written by medical experts; aci conversations
were role-played by a doctor and a lay volunteer from symptom prompts. Notes were
drafted by an automatic note generator, then checked and rewritten by domain experts.
No real patient data.

**Cleaning.** Original data was made for marketing demos and contained imaginary EHR
content. Four annotators with medical backgrounds marked note text unsupported by the
transcript (e.g., invented vitals, treatment reasoning never stated), which was then
removed. Annotators also fixed inconsistent values and ASR-related mismatches.

**Validation.** Medical annotators reviewed every symptom, test, diagnosis, and
treatment. Uncertain items were checked against 3M+ proprietary notes or escalated to
a clinical expert. Medically unsound encounters were removed.

**Structure.** Notes are split into four contiguous SOAP-inspired divisions:
subjective, objective_exam, objective_results, assessment_and_plan.

**Splits.** train, valid, test1, test2, test3, using stratified random sampling so
each subset is represented in every split. Test sets 1–3 came from the MEDIQA-Chat
2023 (ACL ClinicalNLP) and MEDIQA-SUM 2023 (CLEF) shared tasks.

- TODO: split sizes per subset from Table 3 (total believed ~207; confirm).

**Baselines.** Transcript copy-and-paste, retrieval of similar training notes, BART
variants, LED variants, and OpenAI models (text-davinci-002/003, ChatGPT, GPT-4).
Compared full-note vs division-based generation.

**Metrics.** ROUGE-1/2/L (word overlap), BERTScore (embedding similarity), BLEURT
(learned metric), and medcon (F1 over UMLS medical concepts, no negation handling).

### Key findings (with numbers)

- **Annotation agreement:** 0.85 F1 (partial span overlap) for marking unsupported
  text. Even medical experts don't fully agree on what's supported.
- **Best models (test 1, full note):**
  - BART + FT-SAMSum (division-based): best ROUGE (R-1 53.46, R-2 25.08, R-L 48.62).
  - GPT-4: best medcon (57.78), with R-1 51.76, R-L 45.97. No fine-tuning.
- **Metrics are weak proxies for clinical accuracy:** copying the entire transcript
  scored medcon 55.65, close to GPT-4's 57.78 (but ROUGE-L only 30.61). Retrieving a
  different patient's note scored ROUGE-L 40.47 while being factually wrong for the
  patient.
- **Division-based generation helped:** +1 to 14 points on full-note ROUGE and medcon
  for BART/LED models.
- **ASR effect small on metrics:** virtscribe test 1 ROUGE-L dropped from 43.98
  (human transcript) to 41.74 (ASR); aci ASR vs. corrected differed by ~1 point.
  Authors caution metrics weight all facts equally, so clinically important ASR
  errors may be hidden.
- **Realism (20 aci-bench validation encounters vs. 163 real family-medicine
  encounters):**
  - Notes: 492 vs. 683 tokens. Transcripts: 1,203 vs. 1,505 tokens.
  - Aligned note sentences: 0.95 vs. 0.84. Aligned transcript sentences: 0.49 vs. 0.34.
  - Jaccard unigram similarity of aligned segments: 0.12 vs. 0.15 (very low overlap).
  - Crossing alignments: 0.95 vs. 0.67.
  - QA vs. dictation content: 43% vs. 4% (aci-bench) and 15% vs. 8% (real).
  - Conclusion: aci-bench is somewhat shorter and easier, skewed toward QA content.
- **Length limits:** full notes plus references exceed the 512-subtoken limit of
  BERT-based models, so BERTScore/BLEURT were used only per division.

### Limitations

- Small, synthetic, single-institution data (Nuance demo studio, Eastern
  Massachusetts); speech patterns lean US Northeast; creator demographics not recorded.
- Only a handful of note formats; real notes vary far more across providers.
- EHR-sourced content was removed, so the task is conversation-to-note only; real
  notes include vitals, labs, and templates from the EHR.
- One reference note per encounter; no multiple references.
- Realism comparison is small (20 encounters) and uses non-public data.
- Automatic metrics weight all content equally and ignore negation.
- Authors explicitly call for fine-grained definitions of critical vs. non-critical
  hallucinations and omissions as future work. (This is my project's motivation.)

### What this means for my project

- **Design choice it supports:**
  - Separate omission detection with severity grading: in real visits only ~34% of
    transcript sentences reach the note, so flagging every missing fact would flood
    clinicians with false alarms.
  - Hybrid retrieval (BM25 + embeddings): note and transcript wording barely overlap
    (Jaccard ~0.12–0.15), so lexical search alone misses paraphrased evidence.
  - Retrieval before NLI: transcripts (~1,200 tokens) exceed typical ~512-token NLI
    context windows.
  - Negation rules: medcon ignores assertion status, so "no chest pain" = "chest pain."
  - Not using ROUGE/medcon to judge correctness: transcript copying nearly matches
    GPT-4 on medcon.
  - Transcript-derived fact sheets: reference notes are summaries, not complete fact
    inventories. (Revise earlier "reference notes contain discrepancies" rationale;
    the authors removed most unsupported text, though cleanup was imperfect.)
- **Something to reuse:**
  - The four-division scheme: inject errors in every division; report results per
    division; use division as a severity input.
  - The subset metadata column: stratify my dataset by subset and report per subset.
  - Table 2's unsupported-text categories as realistic hallucination injection types.
  - The ASR-corrected aci transcripts as my main evidence source.
  - The authors' regex section-splitting code (study before writing my own).
- **Something to avoid:**
  - Checking notes against raw ASR without a deliberate decision (garbled terms would
    cause false alarms). Candidate for decision 004.
  - Tuning thresholds on the test split (leakage). Use a dev split; group variants of
    the same encounter into one split.
  - Assuming the base notes are perfectly clean: manually audit a sample first.
  - Medically implausible injected errors (enable shortcut detection).
  - Claiming real-world performance: data is synthetic and easier than real visits.
  - Ignoring possible pretraining contamination: the dataset has been public since 2023.

### Terms I looked up

- **Ambient clinical intelligence / ambient scribe:** software that listens to a visit
  and drafts the clinical note.
- **ASR (automatic speech recognition):** speech-to-text.
- **EHR (electronic health record):** hospital's digital patient record system.
- **SOAP:** Subjective, Objective, Assessment, Plan. Standard clinical note structure.
- **Chief complaint (CC) / HPI:** main reason for visit / story of the current problem.
- **Semi-structured document:** has sections and headings, but free text within them.
- **Grounded / supported / faithful:** a statement backed by evidence in the source.
- **Annotation guidelines:** written rules for human labelers.
- **Inter-annotator agreement (IAA):** how consistently annotators label the same data.
- **Span:** a stretch of text defined by start and end positions.
- **Precision / recall / F1:** share of flags that are correct / share of true items
  flagged / harmonic mean of the two.
- **Train / validation (dev) / test split:** learn / tune and select / final unbiased score.
- **Overfitting / generalization:** memorizing training data / performing well on new data.
- **Data leakage (test contamination):** test data influencing development.
- **Stratified sampling / strata:** sampling within groups to preserve proportions.
- **Mixture distribution / mixing weights:** distribution built from weighted components.
- **Distribution shift / subpopulation shift / domain shift:** mismatch between data
  distributions (e.g., benchmark vs. real clinic data).
- **Simpson's paradox:** aggregate results reversing trends seen within groups.
- **Shared task / blind test set:** research competition / test set with hidden answers.
- **Token / subtoken / tokenizer:** text units a model reads / word pieces / splitter.
- **Context window (maximum sequence length) / truncation:** max tokens a model can
  read / cutting off text beyond it.
- **Regex (regular expression):** hand-written text pattern for matching.
- **Alignment annotation:** linking note sentences to their source transcript sentences.
- **Monotonic vs. crossing alignment:** same order vs. reordered content.
- **Jaccard similarity:** shared items divided by total distinct items (0 to 1).
- **Dialogue acts / speech modes:** how something was said (QA pair, statement,
  dictation, statement to scribe).
- **UMLS:** large medical terminology linking synonyms to shared concept IDs.
- **ROUGE / BERTScore / BLEURT / medcon:** word overlap / embedding similarity /
  learned metric / medical-concept F1.
- **Fine-tuning:** further training a pretrained model on a specific task.
- **Hybrid retrieval:** combining lexical (BM25) and embedding-based search.
- **Shortcut learning:** exploiting superficial cues instead of the intended skill.
- **External / ecological validity:** whether results hold in real-world settings.
