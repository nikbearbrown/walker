# Week 02 — Rolling-Horizon Trial

**w/o 2026-07-02**

**Goal:** test `core/gates.md` live — fork gates unfrozen, builder-written goals and prompts, fresh micro-game each. Come out with the **fork logs**, the **excision test results**, and a verdict on whether the fork gate does real work unforced. Kit: `unity/gate-pilot/gate-pilot-week2.md`.

Owners: **B** = Bear · **GA** = Gamer A (Codex) · **GB** = Gamer B (Claude Code) · **✦** = agent.
A **gate** is a hard stop a named human clears (SNICKERDOODLE P4).

## Prerequisite

- [ ] (B) Week-1 debrief done and tooling-gap list captured. Week 2 doesn't start on top of an unfinished week 1 — that would be a direction decision from unsolid ground.

## Trial — the main thing

- [ ] (GA, GB) Write the Gate 0 sentence for a fresh micro-game. *Gate: B reads it and can say what's being built without asking a question.*
- [ ] (GA, GB) Plan horizon 1 — three steps with name / solid bar (qualities, not values) / boundary — **before any prompt**. Partner-check: every bar failable.
- [ ] (GA, GB) Build horizon 1, step-gating each step to solid.
- [ ] (GA, GB) **Fork gate 1** — ground check, play the whole against the Gate 0 sentence, decide stay/fork/kill with a written reason. *Gate: reason references the goal sentence; stays included.*
- [ ] (GA, GB) Plan + build horizon 2, fork gate 2. (Horizon 3 if fast.)
- [ ] (GA, GB) **Excision test** — archive then delete one mid-path step's script; log what breaks.
- [ ] (GA, GB) Keep step logs, fork logs, and tooling-gap additions throughout.

## Repo / doctrine — parallel hygiene

- [ ] (✦/B) Carry over from week 1 if not done: consolidate `core/` doctrine; split Unity-specific pieces into `unity/`; decide vendor-vs-reference for `SNICKERDOODLE.md`.
- [ ] (B) Fold week-2 findings into `core/gates.md` if the doctrine needs amending (horizon size, fork-log fields).

## End of week — debrief

- [ ] (B + gamers) Fork-gate verdict: did it change direction anywhere? Were stay reasons real or rubber stamps? Did fork-from-solid ever bind?
- [ ] (B + gamers) Excision results: were the steps actually separable? Would a real fork have been affordable?
- [ ] (B + gamers) Horizon size: keep three or tune?
- [ ] (B) Merge week-2 tooling gaps with week 1's — the union is the `unity/` build backlog. **This is the fortnight's real output.**
