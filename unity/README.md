# unity/ — Unity domain layer + tooling (built first)

All the real Unity tooling, plus the Unity-specific instantiation of the core doctrine. Anything that names `.meta`, `AssetDatabase`, `.prefab`, `.asmdef`, or scenes lives here, not in `core/`.

## The membrane, here

- **Text layer** — C#, config, `.asmdef`. AI-safe, diffable. The agent works here.
- **Binding layer** — `.meta` GUIDs, `.prefab`, scenes, ScriptableObject `.asset`. Editor-only, or GUID-aware tooling driving Unity's own primitives. The agent never authors these as free text.
- Moves preserve GUIDs: move the file **and** its `.meta` together, or use `AssetDatabase.MoveAsset` via batchmode. Never `mv` an asset without its meta.

## Planned tooling

- **Indexer** — the project map (`unity_project_walker.py` equivalent).
- **Move executor** — manifest → `AssetDatabase.MoveAsset` run through `Unity -batchmode`. Safe by construction, not a filesystem hack around the Editor.
- **CLAUDE.md generator** — audit report → the per-project agent constitution.
- **Verification engine** — characterization / play-test harness. The hardest and most valuable piece; if it works, the product works.

Also lands here as it's written: the A–E phase playbook and the seven Unity failure modes — the Unity instantiation of `core/` doctrine.

## gate-pilot/

The week-1 Codex-vs-Claude greenfield pilot — the first real Unity activity in the repo. Its **tooling-gap list** (everything builders had to do by hand) is the user-written roadmap that seeds the tooling above. Start there, not with the tooling.

## Status

The pilot is ready to run; the tooling is not built. The pilot comes first on purpose — it tells us what to build instead of us guessing.
