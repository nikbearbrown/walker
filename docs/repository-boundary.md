# Walker framework repository boundary

The public Walker repository distributes framework instructions, reusable design
prompts, engine guides, asset-generation tools, and the runtime publisher. Games
are separate repositories; a framework checkout must not require a game checkout.

## Include

- `asset-gen/`: reusable asset-generation instructions, tools, and requirements.
- `engines/`: engine-specific runtime guidance.
- `prompts/`: runtime manifest and Zelda/GDD authoring prompt.
- `scripts/` and `publish.sh`: runtime instruction publishing helpers.
- `docs/`, `setup.md`, and the Godot research/guidance Markdown files.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, contribution/history files, and `LICENSE.md`.

## Keep local or publish separately

- `games/`, `examples/`, and `projects/`: game implementations and game-specific assets.
- `godot-demo-projects/`: downloaded upstream reference projects.
- `youtube/`: film sources, narration, render workspaces, and exports.
- Credentials, installed dependencies, engine/editor caches, builds, and captures.
- Recovered student-submission provenance belongs with its recovered collection,
  not in the framework's licensing declaration. Keep those originals on disk.

The `.gitignore` enforces this boundary without deleting any local examples.
It applies only to untracked files; files already tracked remotely must be
reviewed explicitly. Do not force-push or rewrite history to apply these rules.

Link to example repositories instead of relative paths into ignored folders:

- [Walker Jumpman](https://github.com/nikbearbrown/walker-jumpman)
- [Walker Jumpman Clawd](https://github.com/nikbearbrown/walker-jumpman-clawd)

Before publication, check that every local documentation link resolves in the
publishable file set, review for credentials, and reject files over 25 MB.
Gitignore cannot express a file-size rule; that requires a separate pre-push
audit or automated check. Keep reusable templates, requirements, and source
assets that the framework itself needs; do not blanket-ignore `asset-gen/`,
all images, or all Godot `.uid` / `.import` source metadata.

## Legacy preservation

At inspection on September 11, 2026, this local directory had no `.git` directory.
The existing `nikbearbrown/walker` remote contained an earlier Unity-first
framework (`core/`, `assets/`, `unity/`, `unreal/`, and `todo/`) absent locally.
That complete earlier tree is preserved unchanged under `legacy/`, from commit
`3b394be95d49537cb806317f6f617c4ba20e8bf8`. The active framework now occupies
the repository root, with the original Git history retained. Historical agent
instructions under `legacy/` describe only the archived framework.

The local runtime publisher still supplies its existing C#/.NET Godot guide;
the Zelda/GDD documents describe authoring instructions, not an installed Walker
CLI. Packaging alone does not change those capabilities.
