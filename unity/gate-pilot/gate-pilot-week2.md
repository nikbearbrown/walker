# Week 2 — Rolling-Horizon Trial (fork gates live)

## The experiment

Week 1 tested **step gates** with the path frozen — six increments, fixed order, identical prompts, because the Codex-vs-Claude comparison needed identical paths. Week 2 unfreezes the path and tests the rest of `core/gates.md`: **Gate 0, horizon planning, the fork gate, fork-from-solid, and forkability economics.**

This is **not a head-to-head anymore.** Each builder keeps their week-1 agent (GA → Codex, GB → Claude Code) for familiarity, but goals, prompts, and paths will diverge — divergence is expected and is data, not noise. What's under test is the *doctrine*, run twice.

The week-1 shift builders will feel immediately: **you write the prompts now.** Week 1 handed you six prompts; week 2 hands you a doctrine and a blank page. Formulating the step — deciding what to hand the agent — is the skill this week trains. That's Problem Formulation, and it's harder than it looks.

## Setup

- **Fresh micro-game.** Not the week-1 survivor. One screen, primitives only, no art, no imported assets. Same harness discipline: `unity/UNITY.md` applies in full (Unity 6 LTS, membrane rules, pre-installed libraries, input default).
- Each builder makes their own empty-ish starter (camera, one primitive placeholder, tags as needed). Zero scripts. Ten minutes, not a deliverable.
- Everything agents produce is `.cs` only. Membrane as always.

## Gate 0 — write your goal sentence

Before any prompt, each builder writes **one sentence**:

> **[GAME] is a [what] where the player [core verb], and it succeeds when [the feel/fun condition a player would report].**

Rules: name the *thing*, not a genre vibe. One core verb. The success condition must be judgeable by playing. "A fun little arcade game" fails — it describes ten thousand games. "**Pulse** is a one-button dodger where the player taps to reverse orbit direction, and it succeeds when a 30-second run feels tense but fair" passes.

Seed ideas if stuck (write your own sentence — don't copy these): one-button orbit dodger · pong against a wall that shrinks · flappy-style cave drift · breakout where the paddle shoots · snake that gets faster, not longer.

**Gate 0 clears when Bear reads the sentence and can say what the builder is making without asking a question.** Named human, logged. No prompt exists before this.

## Planning a horizon

Three steps, written down **before any code**, each with:

| Field | Rule |
|---|---|
| **Name** | A nameable unit of the build ("orbit movement", "death + restart") — never "continue" |
| **Solid bar** | The testable adequacy condition you'll play against. **Qualities, not values** — "reversal feels instant, no perceived lag" not "reversal in 0.1s". If the bar can't be failed, it's not a bar. |
| **Boundary** | The one script-unit this step is; what it does *not* touch. This is what makes the excision test (below) survivable. |

**Partner check (cheap, required):** before coding, swap horizon plans. The partner asks one question per step: *"Can this bar be failed?"* Vague bars get rewritten now, not discovered at the gate.

Your prompts are yours to write, but every prompt inherits the week-1 discipline: name the script(s), state the boundary ("do not modify other scripts"), no prefab/scene/`.asset` authoring, output only the code. The step plan *is* the prompt spec — if the prompt is hard to write, the step was underformulated.

## Step gates (as week 1)

Paste → play → back-and-forth → declare **solid / deferred / cut**. Named human, logged. Only solid opens the next step. The step gate asks *is this step solid?* — nothing else.

## The fork gate — the week's centerpiece

After step 3 of every horizon, **unconditionally** — not when something feels wrong, *on cadence*:

1. **Check the ground.** If the last step isn't solid, you may not decide direction yet — solidify or cut it first. No direction decisions on corrupted evidence (fork-from-solid).
2. **Play the whole.** Not the last step — the game so far, against the Gate 0 sentence.
3. **Decide: stay / fork / kill.** Named, logged, **with a written reason — stays included.** A stay whose reason doesn't reference the goal sentence is a rubber stamp, and rubber-stamp stays are the autopilot failure this gate exists to catch.
   - **Stay** → plan the next three steps on this path.
   - **Fork** → keep the solid steps, replace the path from here. Log what the fork cost in time — that number is the forkability economics, measured.
   - **Kill** → goal or approach is wrong. Archive (never delete), write the reason, either re-run Gate 0 with a new sentence or stop.

**Minimum two horizons this week** (six steps), so the fork gate runs at least twice per builder. Three horizons if you're fast.

## The excision test (required, even if nobody forked)

Fork gates might all come up "stay" — fine, that's a finding. But "coded for forkability" gets tested mechanically regardless. **End of week, each builder:**

1. Pick one mid-path step (not the first, not the last).
2. Delete its script(s). (Archive first.)
3. Does the rest compile and run, minus that feature?

Clean excision = the boundaries were real. Compile errors rippling through siblings = the steps were named but not *separated*, and a real fork would have been surgery. Log what broke — this is the doctrine's "sunk cost lives in tangled code" claim, tested.

## Logs

**Horizon plan** (per horizon, before code): the three steps with name / solid bar / boundary, plus partner-check outcome.

**Step log** (per step — trimmed week-1 format): round-trips to solid · what only playing revealed · membrane pressure · gate decision.

**Fork log** (per fork gate — the week's key artifact):

| Field | Capture |
|---|---|
| Horizon # | 1 / 2 / 3 |
| Ground check | last step solid? (if not: what you did first) |
| Decision | stay / fork / kill |
| Reason | written; must reference the Gate 0 sentence |
| Evidence | which step-gate outcomes informed it |
| If fork: cost | time to excise + replan, what survived |

## Hand back

- The micro-game, wherever it ended (unfinished is fine — killed with a good reason is *better* than finished on autopilot).
- Gate 0 sentence + every horizon plan.
- The fork log — complete, stays included.
- Excision test result: what broke.
- Step logs + tooling-gap additions (what you did by hand that a tool should have).
- One paragraph: **was three the right horizon size?** Too short reads as ceremony; too long reads as sunk cost. Say which you felt.

## End-of-week debrief

1. **Did any fork gate change direction?** If all six+ decisions were stay — read the reasons aloud. Real reasons or rubber stamps?
2. **Did fork-from-solid ever bind?** (A shaky step 3 forcing solidify-before-decide.) That rule earning its keep once justifies it.
3. **What did the excision test break**, and would a real fork have been affordable?
4. **Prompts: builder-written vs week-1's handed prompts** — did round-trips to solid change? That's the formulation skill, measured against last week's baseline.
5. **Horizon size:** consensus on three, or tune it?
6. **Tooling gaps** — append to the week-1 list; the union seeds the `unity/` backlog.

The question the week answers: does the fork gate do real work when nobody forces it — or does the direction question still need a human who's willing to ask it against their own momentum?
