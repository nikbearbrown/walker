# assets/ — generative pipeline

Engine-agnostic. Source-media generation that sits *upstream* of both engines and also powers non-engine work (daily videos). Not a peer of `unity/`/`unreal/` — a different axis that feeds them.

## What belongs

- Adapters to asset generators, each behind one interface: Higgsfield (MCP), ElevenLabs (voice), art generators, music. Some speak MCP, some CLI — the integration mechanism is an implementation detail behind the adapter.
- This is **layer 2** (source media: PNG, WAV, music, VO, FBX). Generation is AI-safe and CLI/MCP-native. *Binding* media into an engine — import, GUID assignment, prefab wiring — is **layer 3**, the membrane, and lives in `unity/`/`unreal/`, not here.

## Asset manifest discipline

Every generated file carries provenance: prompt + generator + seed + version → output file → where it bound into the engine. Provenance or it's a pile of mystery files (SNICKERDOODLE P3). The manifest is also the record of what crossed the membrane (layer 2 → 3).

## Status

Stub. Port the existing asset-generation tooling here. This is the one zone with a proven, agent-independent shape already — it predates both engines and serves three consumers (Unity, Unreal, video), so it earns its own folder now rather than waiting for a second engine to reveal the abstraction.
