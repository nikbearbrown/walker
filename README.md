# Walker

Doctrine and tooling for AI-assisted Unity work — refactoring legacy projects and building greenfield ones — with a hard line protecting the parts an AI can't safely touch. Unreal is a later TODO, not a parallel track.

## The core idea

AI made *execution* cheap. It did not make *judgment* cheap. Two ideas follow:

- **The membrane.** A Unity project has a text layer (C#, config) that's diffable and AI-safe, and an asset layer (`.meta` GUIDs, prefabs, scenes) that's binary, reference-by-id, and breaks silently when touched wrong. The agent works the text layer; the human (or GUID-aware tooling, inside the Editor) works the asset layer. The membrane between them is sacred.
- **Conformance vs adequacy.** Code that compiles and runs is *conformance* — a machine can check it. Whether the game *feels* right is *adequacy* — only a human playing it can clear that gate. The CLI cannot play the game.

## Status

Early. This repo is currently **doctrine + a week-1 gate pilot**, not shipped tooling. The `unity/` tooling (indexer, GUID-safe move executor, CLAUDE.md generator, verification engine) is the next build, and its roadmap is being written by the pilot's tooling-gap list rather than guessed.

## Layout

```
core/     # engine-agnostic doctrine only (no .meta / AssetDatabase / MCP)
assets/   # generative pipeline — Higgsfield, ElevenLabs, art, music; also powers video
unity/    # Unity domain layer + tooling, built first; holds gate-pilot/
unreal/   # stub: TODO, integration via MCP
todo/     # the project's own to-do, one file per week (current: week-01.md)
```

Each folder has a `README.md` saying what belongs in it.

## What's here

| Path | What |
|---|---|
| `walker-cli-critique.md` | Whole-project strategy — why Unity-first, why the membrane, what to build and what not to. |
| `unity/gate-pilot/gate-pilot-assignment-week1.md` | The week-1 to-do for two gamers building a tiny Unity game — one on Codex, one on Claude Code. |
| `unity/gate-pilot/gate-pilot-week1.md` | The operating kit: shared harness, six identical prompts, definition-of-solid bars, attestation, P8 earn-silent trial. |
| `core/` · `assets/` · `unity/` · `unreal/` | The four zones, each with a README. Mostly stubs today — the repo is early. |
| `AGENTS.md` / `CLAUDE.md` | How agents operate in this repo. |

## Governance

This repo runs under the Reallocation Engine constitution, `SNICKERDOODLE.md` (canonical home: [nikbearbrown/the-reallocation-engine](https://github.com/nikbearbrown/the-reallocation-engine)). Walker inherits it and adds the Unity-specific domain layer; it does not fork or restate it.
