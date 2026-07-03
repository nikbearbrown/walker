# Gates — the rolling-horizon doctrine

Engine-agnostic. How Walker sequences work: a goal, a short planned horizon, a gate after every step, and a direction decision after every horizon. Every gate is cleared by a named human and logged (SNICKERDOODLE P4). Nothing here names an engine primitive; where the gates physically land (a play-test, a rendered frame, a report) is a domain concern.

## The shape

```
GOAL (Gate 0)
  └─ HORIZON: three named steps, solid bars written before any code
       step 1 → STEP GATE
       step 2 → STEP GATE
       step 3 → STEP GATE
                └─ FORK GATE: stay / fork / kill
                     └─ next horizon (or a different one, or none)
```

Plan only the next horizon. The plan is always short enough that abandoning it is cheap — the point is ten honest versions in the time one over-committed version would take. The full path is never specified upfront, because in feel-driven work the document cannot know what only building reveals.

## Gate 0 — formulation

No prompt is written until a named human has written **one sentence naming the thing being built** — the thing, not the problem it solves; where it sits; what it produces. Agent pressure erodes this gate fastest: an agent will happily generate code for an unformulated goal, and the output will look like progress. A sophisticated build on an unformulated goal is worse than no build — it looks like rigor.

Gate 0 also fixes what the horizon's steps are measured against. A step can only be "toward the goal" if the goal is a sentence, not a vibe.

## Planning a horizon

Three steps (default — see "Why three"), each with, written **before** any code:

- **A name.** The step is a nameable unit of the build, not "continue."
- **A solid bar.** The testable adequacy condition a human will judge it against. Bars name *qualities* ("no drift, stops cleanly, threatening but beatable"), not tuned values — values are discovered at the gate, then locked. Pinning values upfront is specification theater.
- **A boundary.** What the step does *not* touch. One unit, one responsibility, no tendrils into its siblings.

"Looks good" is not a solid bar. If the bar cannot be failed, it is not a bar.

## The step gate

After each step: the machine checks conformance (it builds, it runs), the human checks adequacy (it is *right* — played, watched, read, whatever the domain's oracle is). The human declares **solid / deferred / cut**, by name, logged. Only solid opens the next step.

The step gate asks one question: **is this step solid?** It does not ask whether the path is right. That is a different gate, and mixing them is how the direction question gets skipped.

## The fork gate

After the last step of every horizon — **on cadence, not on suspicion** — a named human looks at the whole and decides:

- **Stay** — plan the next horizon on this path.
- **Fork** — keep the solid steps, replace the path from here. Log why.
- **Kill** — the goal or the approach is wrong. Log why. Archive everything.

The fork gate asks: **is this path still right?** It is an interpretive-judgment and executive-integration decision, not a quality check. It runs even when every step gate was green — *especially* then. Projects die politely when every step passes and nobody's gate ever asks about direction. Wanting to skip the fork gate because "everything's passing" is the autopilot signal it exists to catch.

Fork and kill are successes of the method, not failures of the builder. The failure mode is a human staying on a dead path to avoid logging a fork.

## Fork only from solid ground

The load-bearing rule. **No direction decision on top of an unsolid step.** If the last step is shaky, you cannot tell whether the path is wrong or the step is just badly built — and you may abandon a good path off corrupted evidence. Solidify first, then judge direction. The fork gate consumes step-gate outcomes as its evidence; it does not run without them.

## Coded for forkability

"Named, coded for clarity" is not a style preference — it is what makes the fork gate affordable. A fork keeps steps 1–2 and replaces step 3, which is only cheap if each step is a separable, named unit. Sunk cost does not live in the calendar; it lives in tangled code. If forking means surgery on the survivors, humans stop forking, and the fork gate becomes ceremony.

So the step boundary is enforced at authoring time: one step, one unit, no modification of sibling units unless the step's plan says so. And discarded steps are **archived, never deleted** — a dead fork is data about the path.

## Trust changes gate cost, never gate count (P8)

Earned trust (a VERIFIED skill + attestation) may lighten what *evidence* the human accepts at a step gate — conformance-only, once, as a controlled trial. It never removes the gate, never removes the human's declaration, and never touches the fork gate at all. The gate count is invariant; only the gate cost moves. Any change to the trusted skill revokes the lighter gate. If "earned trust" ever reads as "the gate became optional," that is the rot, not the doctrine.

## Why three

Horizon size is a trade. One step per horizon is pure reactivity — gate overhead dominates and momentum never forms (the "gates as ceremony" complaint is usually a horizon set too short). Many steps is waterfall wearing agile's clothes — by the time the fork gate runs, sunk cost has already voted. Three is the default because it is long enough to build something judgeable and short enough that "throw away this horizon" is a shrug. Domains may tune it; they may not remove the fork gate.

## The two questions, side by side

| | Step gate | Fork gate |
|---|---|---|
| Asks | Is this step solid? | Is this path still right? |
| Kind | Adequacy of the work | Adequacy of the direction |
| Capacity | Plausibility auditing | Interpretive judgment + executive integration |
| Cadence | Every step | Every horizon, unconditionally |
| Outcomes | solid / deferred / cut | stay / fork / kill |
| Cleared by | Named human, logged | Named human, logged |

## Special case: controlled experiments freeze the fork

A head-to-head comparison (same spec, different agents) requires identical paths, so its fork gates are deliberately frozen — the plan is fixed for the length of the experiment and only step gates run live. That is an experimental control, not the doctrine. The general case is the rolling horizon above.
