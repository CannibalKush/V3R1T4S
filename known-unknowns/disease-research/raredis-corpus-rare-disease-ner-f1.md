# RareDis corpus: beat the published BioBERT F1 for rare-disease and sign entity recognition on the fixed test split

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Diagnostic delay in rare disease is partly an information problem: the knowledge sits in unstructured text. Isabel Segura-Bedmar's group at Universidad Carlos III de Madrid released the RareDis corpus - NORD rare-disease texts manually annotated with four entity types (rare disease, disease, sign, symptom) and their relations, with official train/validation/test splits and 9,318 entities - at github.com/isegura/NLP4RARE-CM-UC3M, free to download. Their 2022 study (J Biomed Inform; Europe PMC PMC9258216, open access) benchmarks BiLSTM and transformer models on that fixed split: BioBERT is best with F1 85.2% for rare diseases but only 57.2% for signs, because signs are complex, nested, overlapping and discontinuous noun phrases. A 57% F1 is a long way from saturated, the corpus is a few megabytes, and training a small transformer or a structured span model is laptop work.

## What counts as a win

Success means a released model plus saved per-token/per-span predictions on the OFFICIAL RareDis test split (pinned commit of github.com/isegura/NLP4RARE-CM-UC3M, sha256 of the split files published; no document dropped), trained only on the official training split (the validation split may be used for model selection, the test split for nothing), whose micro-averaged F1 for a named entity type - computed with exact-span matching as in the published evaluation, by a scorer the skeptic reruns - is STRICTLY GREATER (direction: max) than the best published F1 for that entity type, re-read live from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9258216/fullTextXML immediately before claiming (85.2% for rare diseases, 57.2% for signs as read 2026-10-15), by at least 2 points absolute AND outside a 95% bootstrap interval over documents. Precision and recall must be reported with the F1, and the same model must be scored on all four entity types so that a gain on one is not bought by a collapse elsewhere.

## Partial wins

- **p1:** Beat the published sign F1 (57.2% as read 2026-10-15) by >= 3 points on the official test split with the bootstrap interval over documents excluding zero, releasing the per-span predictions.
- **p2:** Match the published rare-disease F1 to within 1 point with a model that runs CPU-only inference over the whole test split in under 60 seconds, with timings - practical for a clinic without a GPU.
- **p3:** An annotation-quality audit: re-examine the spans the best model gets wrong, classify them into annotation inconsistencies versus genuine errors with a published rubric and a second annotator's agreement statistic, and quantify the ceiling the corpus itself imposes.

## How a win is checked

Skeptic clones the corpus repository at the pinned commit, hashes the split files, confirms the attacker's training code never reads the test split (code review plus a run with the test files replaced by scrambled copies, which must leave training outputs unchanged), reruns the attacker's released inference to regenerate predictions, recomputes exact-span micro-F1 per entity type with an independent scorer, bootstraps over documents, and re-reads the published numbers through Europe PMC. Everything is megabytes and minutes on CPU; a small transformer fine-tune is hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9258216/fullTextXML>

## Sources

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9258216/fullTextXML>
- <https://github.com/isegura/NLP4RARE-CM-UC3M>
- <https://zenodo.org/records/10561126>
- <https://rarediseases.org/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Span-based rather than token-based decoding: signs are nested, overlapping and discontinuous, which BIO tagging cannot represent; exhaustive span classification, or a grammar over spans, directly targets the 57% class.
- CROSS-DOMAIN (parsing / formal languages): parse each sentence with a dependency or constituency parser and define entity candidates as syntactic constituents, so discontinuous signs become coordinated subtrees instead of impossible tag sequences.
- CROSS-DOMAIN (information retrieval / ontology lookup): a high-recall dictionary pass over HPO, Orphanet and MONDO labels and synonyms, followed by a learned filter, is a strong and interpretable baseline that neural models rarely beat on recall.
- CROSS-DOMAIN (compression / MDL): choose the span segmentation that minimises description length of the sentence under a two-part code (entity lexicon plus residual text), which penalises overgeneration automatically.
- Data programming: the corpus is small, so weak supervision over unlabelled NORD and Orphanet text (ontology matches, pattern rules, a label model) can multiply effective training data without touching the test split.
- Transfer from clinical NER corpora (BC5CDR, NCBI Disease) with domain-adaptive pretraining on rare-disease text, keeping the RareDis test documents strictly out of every pretraining corpus.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Pretraining contamination: NORD texts are on the public web, so a language model pretrained on recent web crawls may have memorised the very documents in the test split; the claim must state the pretraining corpus and its cutoff.
- Scorer mismatch: exact-span, relaxed-overlap and token-level F1 differ by many points on nested entities; the published numbers are exact-span micro-F1 and the comparison must use the same scorer, rerun by the skeptic.
- Entity-type cherry-picking: improving signs while rare-disease F1 collapses is not a win; all four types must be reported from one model and one run.
- Document-level correlation: sentences inside a document are not independent, so intervals must bootstrap documents, not sentences, in a corpus this small.
- Benchmark-to-clinic gap: better entity recognition on NORD summaries is not a diagnostic system and says nothing about performance on real clinical notes.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/raredis-corpus-rare-disease-ner-f1.md
```

Already set up? Say `run V3R1T4S on raredis-corpus-rare-disease-ner-f1`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `raredis-corpus-rare-disease-ner-f1`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
