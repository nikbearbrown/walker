# Zelda / GDD — Walker design workflow

Status: **authoring instructions and command specification**, September 10, 2026. No `walker` executable or installed `/gdd` adapter is provided by these documents. An agent can use [the Zelda prompt](../prompts/zelda-gdd.md) directly today. The existing `publish.sh` still installs only the asset-generation skill; it does not install Zelda.

Start with the separate worked-example repository: [walker-jumpman brief](https://github.com/nikbearbrown/walker-jumpman/blob/main/GAME-BRIEF.md), [detailed GDD](https://github.com/nikbearbrown/walker-jumpman/blob/main/GDD.md), and [design status](https://github.com/nikbearbrown/walker-jumpman/blob/main/DESIGN-STATUS.json). Example files are not bundled with the framework.

## What Zelda produces

A rough concept becomes a short game brief, then a detailed, Godot-aware GDD. The brief expresses what the player does and why. The GDD specifies the mechanics, boundaries, scene responsibilities, content, failures, and tests. It is a living specification, not a claim that a game exists.

Proposed command surfaces are `/gdd <command>` in an agent session and `walker gdd <command>` in a future local adapter. Short identifiers such as `v1` are aliases, not additional independent commands. For example, a future `/gdd mechanics` is equivalent to `/gdd s1`.

| Phase | Canonical commands and aliases | Output |
|---|---|---|
| Vision | intake/v1, pillars/v2, loop/v3, px/v4 | Brief, design pillars, decisions, experience goals |
| Systems | mechanics/s1, systems/s2, progression/s3, edge/s4 | Behavioral rules, state/dependency models, edge cases |
| World | world/w1, narrative/w2, characters/w3 | Gameplay-relevant setting and story, or reasoned N/A |
| Scope | features/p1, outofscope/p2, technical/p3, risks/p4, openlog/p5 | Bounded MVP, engine contract, risks, decision log |
| Compilation/review | fulldoc/g1, critique/g2, onepager/g3, newmember/g4 | Sixteen-section GDD and targeted review |
| Optional outputs | tasks, edu | Requested production tickets; opt-in educational audit |
| Refinement | logline, fantasy, comparable, looptest, scopecheck, failmodes, changelog, uiux | Focused design improvements |
| Navigation | help, list, show | Workflow help, registry, or a command's requirements |

The supplied Zelda prompt contains 30 design commands; the public reference adds three navigation commands. Its “34 commands” heading does not match that inventory. A future adapter should generate counts and help from one registry.

## Walker handoffs

| Stage | Input and action | Output / boundary |
|---|---|---|
| Game brief | Refine intent into a brief and GDD; make assumptions visible | Human-reviewed target revision before authorized build |
| Build | Implement an approved, bounded slice in Godot | Runnable project plus implementation map, not a completion claim |
| Playtest | Exercise mechanics and observe humans using the game | Recorded attempts, measurements, and human feedback |
| Inspect | Compare observations with requirement IDs | Defects, unresolved design hypotheses, prioritized next change |
| Revise | Propose or implement authorized changes; rerun affected tests | New revision, rationale, updated evidence; approvals may become stale |
| Export | Produce and test the agreed local target | Versioned package and evidence; publication remains separate |

## Files and ownership

New game IDs, directories, and repository names start with `walker-`, per Bear's naming requirement. The first example is the separate `walker-jumpman` repository. Keep game implementations and recovered asset collections outside the tracked framework source.

For `walker-jumpman`, `GDD.md` is the authored specification and `GAME-BRIEF.md` is its concise companion. `DESIGN-STATUS.json` records revision identity, assumptions, and approval/runtime state; it does not duplicate the GDD's narrative. No generated consolidator is installed, so do not label hand-authored content as compiler output.

A future implementation map should connect each feature ID to actual scene/script paths. Keep a proposed path clearly marked until it exists. Test results must refer to the design revision and actual build they exercised. A newer GDD does not retroactively validate an older build.

## Reusable requests

These are natural-language requests an agent can handle with the prompt, not shell commands:

- “Read Zelda's Walker instructions. Turn this concept into a Godot game brief; ask only what materially changes the game.”
- “Expand the brief into the sixteen-section GDD. Label assumptions, specify failure/reset rules, and map mechanics to acceptance tests.”
- “Critique this GDD against the seven Zelda failure modes. Cite the actual sections; do not invent implementation evidence.”
- “Compare these playtest observations with the GDD. Propose the smallest revision that addresses the problem.”
- “Generate production tasks from the approved GDD with dependencies and acceptance criteria.” This last request explicitly authorizes task drafting, not execution.

## Integration work still required

Implement the command adapter, durable gate validation, safe project creation, Godot discovery, test/capture orchestration, and export checks before claiming an automated end-to-end system. Retain upstream Godogen attribution. Do not create host-specific skill directories in this source repository; any future skill installation belongs in the generated game project and must follow the source repository's editing rules.
