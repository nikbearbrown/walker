# Walker

Framework instructions and tools for building games with AI agents. Walker's
working loop is **Game brief → Build → Playtest → Inspect → Revise → Export**.
The agent helps execute and check changes; the human decides what the game
should be and whether it feels right.

This repository contains the framework, not example games, recovered student
assets, downloaded Godot demos, or video production workspaces. Each game has
its own repository and uses a `walker-` name.

## Start here

```bash
git clone https://github.com/nikbearbrown/walker.git
cd walker
```

1. Read the [Zelda/GDD workflow](docs/zelda-gdd-workflow.md) and give your agent
   the [reusable design prompt](prompts/zelda-gdd.md). Refine a concept into a
   brief, a detailed GDD, and a bounded first build.
2. Choose your engine and language, then review [setup](setup.md) and the
   corresponding guide in [engines/](engines/).
3. Use the publisher below to install runtime instructions into a **new,
   separate game directory**. Ask the agent to implement one approved change,
   run the relevant checks, and show the actual result.
4. Playtest, record what did and did not work, and revise one change at a time.
   A successful build is not evidence of a successful human playtest.

## What is implemented

Walker carries the **Godogen** source publisher and asset-generation tools.
`publish.sh` installs an agent manifest, an engine guide, and the `asset-gen`
skill. It does not create a playable game or implement the entire development
loop automatically.

The [Zelda/GDD prompt](prompts/zelda-gdd.md) is usable as authoring instructions
today. The documented `walker gdd` and `/gdd` command surfaces are specifications,
not an installed CLI or slash-command adapter.

### Engine and agent choices

- **Godot:** the bundled publisher currently emits the existing **C#/.NET**
  [engine guide](engines/godot.md). It does not yet select a GDScript guide.
  The separate Walker Jumpman example uses GDScript and regular Godot; do not
  treat the bundled C# setup as a requirement for that example.
- **Bevy:** [Rust engine guide](engines/bevy.md).
- **Babylon.js:** [TypeScript/browser engine guide](engines/babylon.md).
- **Host agents:** Claude Code or Codex.

### Install instructions into a new game project

The publisher needs Bash, Python 3, rsync, and Git. Engine and optional
asset-generation dependencies are described in [setup](setup.md).

```bash
./publish.sh --engine godot --agent claude --out ../walker-my-game
# Alternatively, choose Codex and a different new project directory:
./publish.sh --engine godot --agent codex --out ../walker-another-game
```

Here, “publish” means **write runtime files locally**, not upload to GitHub.
Use a fresh destination: the publisher replaces generated skill content, and
`--force` deletes the entire destination. Keep framework source and game work
in separate repositories. Review the generated game's `.gitignore` before
publishing it; its defaults exclude generated instructions and Godot assets.

Asset-generation tools can call paid services. They are optional, require your
own credentials, and must not be run without approval for the associated spend.
Never commit credentials.

## Repository map

| Path | Purpose |
| --- | --- |
| [asset-gen/](asset-gen/) | Reusable asset-generation skill, tools, requirements |
| [engines/](engines/) | Engine-specific runtime guidance |
| [prompts/](prompts/) | Runtime manifest and Zelda/GDD authoring prompt |
| [scripts/](scripts/) | Template and agent-metadata rendering helpers |
| [publish.sh](publish.sh) | Install runtime instructions into a separate game |
| [docs/](docs/) | Design workflow, technical guidance, and source notes |
| [setup.md](setup.md) | Host dependencies and optional service configuration |
| [legacy/](legacy/) | Preserved Unity-first Walker framework; historical reference |

Further Godot guidance: [asset organization](godot-asset-organization-report.md),
[organization research prompt](godot-asset-organization-research-prompt.md),
[scripting conventions](godot-scripting-conventions-research-prompt.md), and
[GDScript/C# comparison](docs/gdscript-vs-csharp.md).

## Example games — separate repositories

- [Walker Jumpman](https://github.com/nikbearbrown/walker-jumpman)
- [Walker Jumpman Clawd](https://github.com/nikbearbrown/walker-jumpman-clawd)

Clone examples separately. The local `games/`, `examples/`, `projects/`,
`godot-demo-projects/`, and `youtube/` directories are excluded from this
framework repository. See the [repository boundary](docs/repository-boundary.md).

## Legacy and attribution

The prior Unity-first framework is preserved unchanged under [legacy/](legacy/),
from commit `3b394be95d49537cb806317f6f617c4ba20e8bf8`. Its original README and
agent instructions describe that historical tree, not the active framework.
The original Git history remains intact.

The active publisher, engine guides, and asset-generation tooling retain their
Godogen attribution. See [LICENSE.md](LICENSE.md), [CHANGELOG.md](CHANGELOG.md),
[CONTRIBUTING.md](CONTRIBUTING.md), and [AGENTS.md](AGENTS.md).
