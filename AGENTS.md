# AGENTS.md

Operating instructions for any agent (Claude Code, Codex, or other) working in this repo. Agent-neutral on purpose: Walker is built by **both** Codex and Claude, and **no agent owns an artifact here.**

## What this repo is

Walker — the doctrine and (eventually) the tooling for AI-assisted Unity work: refactoring legacy projects and building greenfield ones, with a hard line protecting the parts AI can't safely touch. Unreal is a later TODO, not a parallel track. Today the repo is **documents**; the `unity/` tooling does not exist yet. Don't add machinery that governs code that isn't here.

## Governance — inherits SNICKERDOODLE, does not fork it

This repo runs under the Reallocation Engine constitution, `SNICKERDOODLE.md` (canonical home: `nikbearbrown/the-reallocation-engine`). **Inherit it; do not restate or fork it** — a second copy is the drift problem, not a convenience. The principle that governs everything here:

> **P1 — machines verify conformance, humans verify adequacy.** Code compiling and running is conformance (machine-checkable). Whether a game *feels* right — not too floaty, fire rate not a machine-gun, no jitter — is adequacy, and only a human playing it can clear that gate. The CLI cannot play the game.

Also live here: **P2** (stored skills before ad-hoc code), **P4** (gates are hard stops cleared by a named human), **P8** (trust is earned by a VERIFIED skill + attestation, not set by a flag).

## The membrane (Walker's domain rule)

- **Text layer** — C#, config. AI-safe, diffable. The agent works here.
- **Asset / engine-binding layer** — `.meta` GUIDs, `.prefab`, scenes, ScriptableObject `.asset`. Human-in-Editor (or GUID-aware tooling) only. The agent never authors these as free text.
- Moves preserve GUIDs (move the file **and** its `.meta` together, or use `AssetDatabase.MoveAsset`). Never `mv` an asset without its meta.

## Layout

```
core/     # engine-agnostic doctrine only. If a file says .meta, AssetDatabase, or MCP, it does NOT belong here.
assets/   # generative pipeline (Higgsfield, ElevenLabs, art, music). Upstream of both engines; also powers video.
unity/    # Unity domain layer + tooling, built first. Holds gate-pilot/.
unreal/   # stub: TODO, integration via MCP. Nothing else yet.
```

Each folder has a `README.md` stating what belongs in it. The doctrine is not yet consolidated into `core/` — see `core/README.md`.

## Read order

1. `README.md` — orientation.
2. `walker-cli-critique.md` — the strategy behind the repo's shape (whole-project; Unity-first, the membrane, the zones).
3. `unity/gate-pilot/gate-pilot-assignment-week1.md` — the week-1 gamer to-do.
4. `unity/gate-pilot/gate-pilot-week1.md` — the operating kit (harness, six prompts, attestation, P8 trial).

## Operating rules

- **Keep skills and recipes agent-neutral.** A Unity recipe, never "Claude's" or "Codex's." Record which agent drafted it as provenance only.
- **Markdown is the default** output format unless asked otherwise.
- **Don't delete** source, docs, or logs — archive instead.
- **Keys/secrets:** none in this repo today. When tooling lands (asset gen via Higgsfield/ElevenLabs, Unity batchmode), secrets go in `.env` (already gitignored) and are **never committed**. If you need a key, read it from the environment; do not hardcode or echo it into a tracked file.
- **Don't over-build.** Add governance machinery (conformance scripts, data contracts, generated instruction pipelines) only alongside the code or data it governs — not before.
