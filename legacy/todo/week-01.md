# Week 01 — Run the Gate Pilot

**w/o 2026-06-25**

**Goal:** run the Codex-vs-Claude gate pilot end to end and come out with two things — the **tooling-gap list** and at least one **VERIFIED skill**. The game itself is the vehicle, not the goal.

Owners: **B** = Bear · **GA** = Gamer A (Codex) · **GB** = Gamer B (Claude Code) · **✦** = agent.
A **gate** is a hard stop a named human clears (SNICKERDOODLE P4).

## Pilot — the main thing

- [ ] (B) Build the shared starter harness — primitive Player / Enemy / Projectile, tags set, prefab shells, **zero scripts**. *Gate: both gamers start from a byte-identical clone.*
- [ ] (B) Hand each gamer the to-do + kit; assign GA → Codex, GB → Claude Code.
- [ ] (B, GA, GB) Lock shared tuned values as they're hit — `moveSpeed`, `fireRate`, `chaseSpeed` — so both judge "solid" against the same numbers.
- [ ] (GA, GB) Build the game, six gated increments, play-test each to *solid* before advancing.
- [ ] (GA, GB) Produce ≥1 **agent-neutral** skill and walk it to VERIFIED. *Gate: attestation includes a deliberate break attempt + an honest "Did not test."*
- [ ] (GA, GB) Run the **P8 earn-silent trial** once the first skill is VERIFIED; record held-or-broke.
- [ ] (GA, GB) Keep the **tooling-gap list** — every "had to do this by hand because no tool did it."

## Repo / doctrine — parallel hygiene

- [ ] (✦/B) Consolidate `core/` doctrine into an engine-agnostic doc: five capacities, boondoggling, gate-as-rhythm, conformance vs adequacy, the abstract membrane.
- [ ] (✦/B) Split the Unity-specific pieces (A–E phases, the seven Unity failure modes, the labor table) out into `unity/`.
- [ ] (B) Decide: **vendor** `SNICKERDOODLE.md` into walker, or keep **referencing** the engine repo. (self-contained vs single-source-of-truth)
- [ ] (B) Optional: start porting asset-gen tooling into `assets/`.

## End of week — debrief

- [ ] (B + gamers) Head-to-head debrief: round-trips to solid, failure shape (Codex vs Claude), membrane discipline, where the gate caught a real problem vs. felt like ceremony.
- [ ] (B) Turn the tooling-gap list into the first `unity/` build backlog. **This is the week's real output.**

## Done this week

- [x] Repo scaffolded — `core/ assets/ unity/ unreal/` zones with READMEs, governance files (`AGENTS.md`, `CLAUDE.md`, `.gitignore`), gate-pilot kit + gamer to-do, pushed to GitHub.
