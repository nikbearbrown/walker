# Research Prompt: How Does Godot Want Assets Organized?

## The Core Problem

Godot is unusual among game engines in that it has **no opinion enforced by the engine** about folder structure — no asset database, no metadata layer sitting above the filesystem the way Unity's `.meta` files do. `res://` *is* the filesystem, and Godot reads it as-is. That freedom is the trap: developers coming from Unity or Unreal expect the engine to have a canonical answer ("put everything under `Assets/`"), and Godot's docs explicitly say there isn't one. What *does* constrain you is a set of engine mechanics that behave differently depending on how you organize things — the import pipeline, the `.import`/`.godot` cache, the UID system introduced in 4.0 and made mandatory-feeling in 4.4, and the fact that Godot is scene-based, so most of what would be a "prefab" or "asset reference" in another engine is actually baked into a `.tscn` file. A good answer to "how should I organize assets" has to explain both the *convention people converge on* and the *mechanical reasons certain choices break or don't break* — because that second part is what changes across Godot versions and what most LLM-generated advice gets wrong (particularly anything trained before Godot 4.4's UID rollout).

This isn't a style question with one right answer; it's an evolving-engine-mechanics question with a loose convention layered on top. The research below separates the two.

---

## 1. What the Engine Actually Enforces (vs. What's Convention)

**Implementation notes:**
- Godot places **no restriction** on directory layout. `res://` can be flat, deeply nested, type-based, or feature-based — the engine doesn't care.
- What *is* mechanical, not stylistic:
  - Files placed inside `res://` are auto-imported if they're a recognized resource type (image, audio, 3D model, font, etc.). Imported data is cached in `res://.godot/imported/` (Godot 4) — this folder should never be hand-edited or relied upon for direct access.
  - A `.gdignore` empty file in a folder tells Godot's importer to skip that folder entirely — useful for docs, source assets you don't want re-imported, or third-party build artifacts.
  - `res://addons/` is the conventional (not mechanically required, but tooling-expected) location for third-party plugins and editor addons — the FileSystem dock, plugin loader, and asset-lib installs all assume this.
- Practical implication: because nothing is enforced, the actual constraint you're organizing around is **"what will make refactors and version control painless as the project scales,"** not "what will make the engine run."

**Code/config example — ignoring a folder from import:**
```
res://
├── docs/
│   ├── .gdignore        # empty file — tells Godot to skip this folder on import
│   └── design_notes.md
```

---

## 2. Scene-Based Architecture Changes What "Asset" Even Means

**Implementation notes:**
- Unlike Unity (GameObject + component data spread across the scene file, referencing separate prefab assets) or Unreal (Blueprints as standalone assets), Godot bakes most configuration *into the scene* (`.tscn`) or resource (`.tres`) file itself. There is comparatively little "loose" asset data sitting outside scenes.
- Because of this, the official Godot docs recommend organizing around **scenes and their immediate dependencies**, not around asset *type*. The canonical example from the docs: put a character's textures, animations, and sounds in the same folder as `character.tscn`, rather than splitting them into project-wide `textures/`, `sounds/`, `animations/` folders.
- Exception carved out explicitly in the docs: **third-party assets** — even if they belong conceptually to one character or feature — often make more sense colocated with that feature's folder rather than dumped generically into `addons/`, *unless* they're a proper plugin.

**Code/config example — feature-colocated structure (docs-recommended default):**
```
res://
├── player/
│   ├── player.tscn
│   ├── player.gd
│   ├── player_sprite.png
│   ├── jump.ogg
│   └── run_anim.tres
├── enemies/
│   └── goblin/
│       ├── goblin.tscn
│       ├── goblin.gd
│       └── goblin_sprite.png
```

---

## 3. Type-Based Structure — The Common Alternative for Larger/Team Projects

**Implementation notes:**
- Despite the docs' scene-colocation recommendation, a large fraction of real-world templates and community advice (Reddit's r/godot, various starter templates) converge on a **type-based top level** (`assets/`, `scenes/`, `scripts/`) with **feature-based subfolders inside each**, especially once multiple people or a large asset count are involved.
- This isn't a rejection of the docs' advice so much as a different scaling strategy: type-first helps discoverability ("where are all the textures") and plays well with import-setting presets applied per-folder (e.g., all textures under `assets/textures/` sharing the same compression settings), while feature-first helps encapsulation and makes it trivial to delete/export a whole feature.
- There is **no consensus** in the Godot community the way there is, say, for Java package conventions — multiple maintainers and forum threads say this explicitly. Treat any single structure (including AI-generated ones) as a starting proposal to adapt, not a spec to follow literally.
- A commonly cited hybrid for larger 4.x projects nests by type at the top and by feature underneath:

**Code/config example — type-first / feature-nested hybrid (common for larger projects):**
```
res://
├── addons/                  # third-party plugins only
├── assets/
│   ├── textures/
│   │   ├── characters/
│   │   ├── environment/
│   │   └── ui/
│   ├── models/
│   ├── audio/
│   └── fonts/
├── scenes/
│   ├── levels/
│   ├── ui/
│   └── characters/
├── scripts/
│   └── autoload/
└── project.godot
```

**Naming convention notes (fairly consistently agreed on across templates):**
- Directories: `snake_case`, always lowercase (`assets/`, `enemy_types/`)
- Scene/script files: `snake_case` matching the root node (`player.tscn`, `player.gd`)
- Root node names inside scenes: `PascalCase` (`Player`, `MainMenu`)

---

## 4. The UID System (Godot 4.0 → 4.4+) — Why Moving Files Is Safer Now, But Not Automatic

**Implementation notes:**
- This is the part of "how Godot wants assets organized" that is **genuinely version-dependent** and where outdated (pre-2024) advice, including from general-purpose AI tools, will actively mislead you.
- Godot 4.0 introduced partial UID (Unique Identifier) support so resource references could survive being moved on disk. Godot 4.4 made this far more complete: scenes and resources now store a `uid://...` reference *alongside* the path, and the editor uses the UID as the source of truth, falling back to path only if the UID is invalid.
- Imported resource types (images, models, audio) store their UID inside the accompanying `.import` file. Native Godot formats (`.tscn`, `.tres`) store the UID directly in their own file header. **Scripts and shaders are plain text and aren't "imported,"** so as of 4.4 they get a separate sidecar `.uid` file that must travel with the script if you move or rename it outside the editor.
- Practical consequence for organization: reorganizing folders **inside the Godot editor** (drag-and-drop in the FileSystem dock) is now much safer than it used to be — Godot updates references automatically. Reorganizing **outside the editor** (via OS file manager, git operations, or a non-Godot-aware script/AI tool) risks orphaning `.uid` sidecars for scripts/shaders, which breaks references silently until you reopen the project and re-save affected scenes.
- If you're using any AI coding assistant to refactor a Godot 4.4+ project's folder structure, this is the single most likely failure mode: the assistant moves `player.gd` but not its `player.gd.uid`, and scene references quietly break.

**Code/config example — what a moved script needs to bring with it (4.4+):**
```
# Before move:
res://scripts/player.gd
res://scripts/player.gd.uid      # must move together with the .gd file

# After move — both files relocate together:
res://player/player.gd
res://player/player.gd.uid
```

---

## 5. Version Control Implications

**Implementation notes:**
- `res://.godot/` is the editor's local cache (imported resource cache, UID cache, etc.) and is excluded from version control by Godot's default `.gitignore` on project creation.
- `.import` files (metadata per imported resource) are conventionally **committed**, not ignored — omitting them causes UID resolution problems and can make a freshly cloned project's editor freeze or behave inconsistently until it fully re-imports, per multiple forum reports on Godot 4 projects.
- As of 4.4, `.uid` sidecar files for scripts/shaders should also be committed — they're tiny (tens of bytes) and are load-bearing for reference resolution, not disposable cache.
- Net guidance: don't treat everything with a leading dot as "ignorable build cruft." `.godot/` → ignore. `.import` and `.uid` → commit.

---

## Standalone Copyable Prompt

```
Research and explain how the Godot game engine (specifically Godot 4.4+) expects
game assets to be organized in a project's res:// filesystem. Cover:

1. What the engine actually enforces mechanically vs. what is pure convention
   (no asset database, no metadata layer above the filesystem, .gdignore behavior,
   the addons/ folder convention).
2. Why Godot's scene-based architecture (as opposed to Unity/Unreal-style separate
   prefab/asset references) leads the official docs to recommend colocating assets
   with the scenes that use them, rather than organizing by file type.
3. The competing type-based folder convention (assets/, scenes/, scripts/) commonly
   used in larger or team projects, including common naming conventions (snake_case
   directories and files, PascalCase root nodes).
4. The Godot 4.0-4.4 UID system: how uid:// references work, what's stored in
   .import files vs. .uid sidecar files vs. scene/resource headers, and why moving
   files outside the editor (including via AI coding assistants not aware of Godot
   4.4 conventions) can silently break references if .uid sidecars aren't moved
   along with their scripts/shaders.
5. Version control implications: what belongs in .gitignore (.godot/) vs. what
   should be committed despite looking like generated cruft (.import files,
   .uid sidecar files).

Cite the specific Godot version where behavior changed (especially the 4.4 UID
rollout), and flag anywhere that pre-4.4 advice would now be outdated or wrong.
```

---

## Reference Lineage / Further Reading

- Godot Docs — Project organization (official best-practices tutorial): `godot-docs/tutorials/best_practices/project_organization.rst`
- Godot Docs — Introduction to best practices series (4.3): `docs.godotengine.org/en/4.3/tutorials/best_practices/introduction_best_practices.html`
- Godot Docs — Importing assets / import process: `docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html`
- Godot Engine blog — "UID changes coming to Godot 4.4": `godotengine.org/article/uid-changes-coming-to-godot-4-4/`
- Godot Docs — `.tscn` file format internals (UID header, format version): `github.com/godotengine/godot-docs/blob/master/contributing/development/file_formats/tscn.rst`
- ResourceUID class reference: `docs.godotengine.org/en/stable/classes/class_resourceuid.html`
- DEV Community — "Godot 4.4 Added .uid Files Everywhere. Here's What They Actually Do." (practical/implementation-level explainer, includes AI-tooling caveat)
- Community templates showing the type-based/hybrid convention in practice: `github.com/theowiik/godot-template`, `github.com/SamuelAsherRivello/godot-project-template`
- Godot Forum threads showing the lack of consensus firsthand: "Godot project structure" (95746), "Folder structure for large game in Godot 4.5" (119115), "Are .import and .godot files+dirs now required in v4?"
