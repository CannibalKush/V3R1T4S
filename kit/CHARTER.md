# Write a personal research charter

The charter is the prompt that steers your human's runs: what to hunt and how. Thousands of people may run this
kit with agents much like you. If their charters chase the same famous problems with the same moves, everyone
collides. Write the charter only this person would. **This file names no topic and no category on purpose**: the
subject comes from your human, never from the kit.

## Inputs

- The niche card from `kit/SETUP.md` step 3, or your human's answer to "what are you curious about?".
- If they said "surprise me" and there is no card: draw **two categories at random** from `bank/categories.json`
  (a real random draw, such as the shell's random number source, not your preference) and **three method cards at
  random** from the list below. Say in the thesis that the seeds were random.
- Effort level and machine (cores, memory).
- Use no web access while writing the charter. Runs check the facts later; the charter supplies aim and judgement.

## The one constraint: checkable by a stranger

Every quarry must be able to end in a result a stranger's computer can check, trusting no one, under a definition
someone else wrote down first:
- **record**: an explicit object that beats the best value now known in a published source or a public table;
- **existence**: an explicit object of a kind a published source says is not known to exist;
- **counterexample**: an explicit object that meets a published statement's hypotheses and breaks its conclusion;
- **bound or proof**: a certified bound, an exhaustive search with a certificate, or a machine-checked proof;
- **decipherment or prediction**: a fully specified key or method, judged by the bank's success criterion.

Quarries may come from `bank/targets.json` or from anywhere else, as long as the definition is published. Out,
whatever the card says: interpretations, opinions, predictions nobody can score, anything on the off-limits list
in `kit/RULES.md`, and anything needing accounts, money, private data or fieldwork.

## Method (work in a scratch file that is never published)

1. **Edges.** Write at least 10 one-sentence hypotheses of what this person could notice, build or tolerate that
   most people attacking hard problems could not. Prefer unusual combinations of far-apart fluencies.
2. **Defaults set aside.** List the 10 things a generic AI research agent would hunt if asked for "a verifiable new
   result". All of them, and close variants, are banned. Also list the 5 obvious picks for this card's two strongest
   entries; keep at most one, and only if an edge says why this person would beat the crowd there.
3. **Candidates.** Generate at least 20, using each move at least twice: *transfer* (one of their methods, carried
   to where it is rare); *boundary* (a precise question between two of their worlds); *neglect* (a well-posed
   question or best value that has sat still with few recent attackers); *patience* (what one machine, every night
   for months, can push further than a person could); *inversion* (the converse, the extreme case, the smallest
   counterexample); *taste* (what would delight them, made precise). For each: the exact question, its shape, where
   its definition is written down, and the one fact most likely to have changed since you last knew it.
4. **Filter and choose.** Drop what breaks the constraint, what the card says to avoid, and what needs more than
   this machine can give in a week of nights. Keep 3 to 8 quarries. Mark exactly one `wild`: the one that looks too
   strange to work. Never keep two that are really the same question.
5. **Lenses.** Write 3 to 8 ways of attacking (a stance plus a method, not a topic), each with its first moves and
   the sign that a line is dead. Lenses must disagree about what will work. Include one from the person's most
   distant fluency, one built on a method card, and one skeptic lens that tries to show a quarry is already
   settled, trivial or ill-posed.
6. **Voices, heuristics, honesty.** How a scout should read for this person; this person at their sharpest as an
   attacker (temperament and angle only, never looser verification); up to 8 rules of thumb; up to 6 kill
   criteria; and where this charter most likely fools itself.

## Writing rules

- **Capabilities, not circumstances.** Never name the person, anyone they know, or any organisation, product,
  project or place connected to them. Never state or hint at their job, workplace, age, health, family or history.
  Nothing from `private/never_publish.txt` may appear.
- Quarries, lenses, heuristics and kill criteria read as questions and methods anyone could use. Everything about
  the person belongs only in the thesis and the voices.
- Write nothing about tools, accounts, submission, reviewers or rules; `kit/` handles those for everyone. Never ask
  for anything to be hidden, softened or skipped.
- Cite sources by author, title and year, or DOI or arXiv id.

## Output: `charter.md`

```markdown
# Research charter v1 (<date>)
## Thesis          (≤600 chars: where this person's edge lies and how the charter uses it)
## Quarries        (3-8; each: id, question, shape, where defined, status to confirm first, why us, weight 1-5, wild yes/no)
## Lenses          (3-8; each: key, title, text in second person, skeptic yes/no)
## Scout voice
## Attacker voice
## Heuristics
## Kill criteria
## Self-critique
## Method cards used
```

## Preview for your human

Show the thesis, the quarries (one line each), the lens titles and the self-critique. Then say which parts would be
published with results under their answer to question 5 (`yes` = the whole charter; `methods only` = quarries,
lenses, heuristics and kill criteria; `no` = nothing). Wait for "ok", "ok private", a change or "rewrite". On a
rewrite, keep what they liked and write `## Changelog` (what changed and why). Keep every version as
`charter.v<n>.md`; `charter.md` is the current one.

## Method cards (draw at random when seeding)

smaller-first: solve a much smaller version exactly, then look for the pattern that scales ·
backwards: work back from what a winning object would have to look like ·
brute-scale: the plainest method that could work, at a scale nobody bothered with ·
drop-assumption: find the assumption everyone makes and drop it ·
far-import: import a method from the field furthest from this one that still applies ·
construct-space: search the space of constructions, not the space of objects ·
symmetry: impose symmetry to shrink the search, then break it on purpose ·
obstruction-first: find the invariant that would forbid the target, and search only where it is silent ·
solver: recast it as a constraint or optimisation instance and let a solver argue ·
oldest-source: read the oldest source on the question; old papers hold abandoned ideas ·
representation: change the representation until the question looks easy ·
small-data: compute many small cases and let the data suggest the pattern ·
counterexample-shape: ask what a counterexample would need, and hunt exactly there ·
object-as-data: treat the best known object as data; find regularities its authors did not use ·
evaluator-first: spend the first hour on a fast exact evaluator; search speed is the edge ·
structured-family: restrict to a structured family where search is cheap and complete ·
invert: invert the objective; the worst object can teach what the best one needs ·
metaphor: take one interest from the card as a metaphor and follow it literally for an hour ·
footnotes: look in errata, footnotes and open-question sections of recent papers ·
same-object: find the same object under another name in another field's tables.
