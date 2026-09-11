# core/ — doctrine only

Engine-agnostic doctrine. The persona, the five supervisory capacities, the gate-as-rhythm, boondoggling, conformance-vs-adequacy, the *abstract* membrane concept (text layer vs binding layer), the labor-separation *principle*, and manifest/report schemas described as docs.

## The rule

**If a file mentions `.meta`, `AssetDatabase`, `.prefab`, `MCP`, or any other engine primitive, it does NOT belong here.** That file is a domain layer — it lives in `unity/` or `unreal/`. Core is what stays true no matter which engine is underneath. The moment doctrine names a Unity or Unreal specific, it has graduated out of core.

## What belongs

- The five supervisory capacities — Plausibility Auditing, Problem Formulation, Tool Orchestration, Interpretive Judgment, Executive Integration.
- Boondoggling — conducting an agent by assigning each task to the right labor and gating by dependency.
- The gate as a rhythm: bound the agent's output → human verifies what the agent can't perceive → don't advance until solid. (Same loop, greenfield or refactor; only the reference oracle differs — invariance vs intent.)
- Conformance vs adequacy: the machine half and the human half of every gate.
- The membrane *as a concept* — a text layer the agent works and a binding layer it must not. Where the membrane physically sits is a domain concern, not a core one.

## Inherits, does not fork

Core sits on top of `SNICKERDOODLE.md` (the Reallocation Engine constitution). Walker doctrine is the *supervisory methodology*; SNICKERDOODLE is the *human–AI contract* (P1–P8). They are different documents — don't restate the constitution here.

## What's here

- **`gates.md`** — the rolling-horizon gate doctrine: Gate 0 (formulation), three-step horizons with step gates, the fork gate (stay/fork/kill), fork-only-from-solid, coded-for-forkability, and P8 as gate-*cost*-never-gate-*count*. The gate-pilot is its frozen-fork special case.

## Status

The rest of the doctrine is **not yet consolidated**. It currently lives scattered across `../walker-cli-critique.md` (strategy) and the original Walker system prompt. Writing the clean engine-agnostic doctrine doc — and splitting the Unity-specific pieces (the A–E phases, the seven Unity failure modes, the labor table) out into `unity/` — is this folder's next task.
