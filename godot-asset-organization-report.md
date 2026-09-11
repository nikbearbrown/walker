# How Does Godot Want Assets Organized?

**Filesystem conventions, import metadata, UIDs, scenes, and safe refactoring in Godot 4.4–4.7**

- **Research date:** September 4, 2026
- **Version scope:** Godot 4.4 through current stable 4.7.2

> Organize around ownership and dependency locality, then preserve the metadata that keeps those dependencies intact.

---

## Direct Answer

Godot does not require an `Assets/` directory or a canonical hierarchy. The folder containing `project.godot` is the project root and therefore `res://`. Within that root, Godot's own best-practices guide recommends keeping assets as close as practical to the scenes that use them. The most reliable default is therefore a **hybrid, feature-first layout**:

1. Keep a scene, its script, and resources private to that feature in the same feature folder.
2. Move a resource to a shared folder only when it is genuinely shared across features.
3. Put reusable systems in clearly bounded system folders, and editor plugins or portable packages under `addons/<package_name>/`.
4. Keep documentation, builds, raw production files that Godot should not scan, and unrelated tooling outside the Godot project root when possible. Use `.gdignore` only when those files must remain under `res://` and truly must not be loadable or exported.

This is a convention, not an engine mandate. The hard constraints come from imports, UIDs, literal paths, case sensitivity, export selection, and scene/resource serialization.

The other central conclusion is that the official phrase "without metadata or an asset database" is now only directionally true. Godot has no Unity-style database that owns a virtual hierarchy above the filesystem, and it does not create one universal `.meta` file for every asset. Modern Godot nevertheless uses substantial metadata:

5. Imported source assets have adjacent `.import` files.
6. Scripts, shaders, and other resource types that cannot embed a UID can have adjacent `.uid` files.
7. `.tscn` and `.tres` files embed their own resource UIDs.
8. `.godot/` contains generated import outputs and project caches, including UID mappings.

The filesystem is authoritative for **location**. Sidecars and embedded IDs are authoritative for **import settings and durable identity**. The generated `.godot/` directory is **disposable cache**.

---

## Scope and Assumptions

This report answers two different questions that are often collapsed into one:

1. What directory structure does Godot require mechanically?
2. What directory structure is the best default for people maintaining a real project?

It focuses on project resources under `res://`, import artifacts, resource identity, scene composition, file moves, source control, and export behavior. It does not attempt to prescribe a genre-specific software architecture or cover platform SDK layouts in detail.

---

## 1. What Godot Actually Requires

### `project.godot` defines the root

Godot treats any folder containing `project.godot` as a project. That folder becomes `res://`; no `Assets/`, `Content/`, or `Source/` child is required. The Godot 4.7 file-path documentation states that every project-relative file is addressed from this root. In an exported game, `res://` is generally read-only; persistent writes belong under `user://`.

This makes repository layout a useful design choice. A repository may place the Godot project at its root, or it may place it in a child such as `game/`. The second form keeps repository documentation, DCC automation, build outputs, and other non-game material outside Godot's scanner without needing `.gdignore` files.

### Files must be visible to the project to become normal resources

The current import-process documentation says importable assets are placed directly inside the project folder. Godot detects them, records import configuration in an adjacent `<asset>.import` file, and stores the platform-ready result in `res://.godot/imported/`. Code should load imported resources through `ResourceLoader`, `load()`, or `preload()`, not by opening the generated imported file directly.

A `.gdignore` file changes more than editor visibility. According to the project-organization guide, a folder containing `.gdignore` disappears from the FileSystem dock, is not imported, and its contents cannot be accessed with `load()` or `preload()`. The import guide also says ignored contents are excluded from export. `.gdignore` is therefore a hard project boundary, not a cosmetic hide rule, and it does not support `.gitignore`-style patterns.

### Names become case-sensitive in the places that matter

Windows and common macOS filesystems are usually case-insensitive, but Linux and Godot's exported PCK filesystem are case-sensitive. The official guide recommends lowercase `snake_case` for folders and files, except where language conventions such as PascalCase C# filenames apply. A path that happens to load as `res://UI/Icon.png` on a developer's machine can fail after export if the actual name is `res://ui/icon.png`.

---

## 2. Godot Is Filesystem-First, Not Metadata-Free

The official project-organization page still says Godot uses the filesystem "as-is, without metadata or an asset database." That sentence describes the architectural contrast with Unity, but it is no longer literally complete. The current import guide calls `.import` files "important metadata," and Godot 4.4 added `.uid` sidecars for resources that cannot store identity internally.

The practical model is:

| File or directory | What it does | Version-control treatment | Move/copy consequence |
|---|---|---|---|
| `project.godot` | Defines the project and the `res://` root | Commit | Keep at the intended project root |
| `.tscn`, `.tres` | Text scenes/resources; embed their own UID and may contain subresources | Commit; prefer text for collaboration | Moveable by UID-aware tooling; an external copy can duplicate an embedded UID |
| Source asset (`.png`, `.glb`, `.wav`) | Human-authored import source | Commit, often with Git LFS when large/binary | Its adjacent `.import` carries settings and identity |
| `<asset>.import` | Import settings, checksums, remapping information, and UID for an imported resource | Commit | Move it with the source; do not discard it as cache |
| `script.gd.uid`, `shader.gdshader.uid` | Durable identity for resource types that do not embed a Godot UID | Commit | Move it with the source; do not copy it when creating a distinct resource |
| `.godot/` | Generated imports, caches, editor state, credentials | Ignore | Safe to regenerate; never treat `uid_cache.bin` as source of truth |
| `.gdignore` | Prevents Godot from scanning, loading, and exporting a subtree | Commit if intentional | Everything below becomes unavailable as a normal project resource |
| `addons/<name>/` | Standard location for editor plugins and a conventional home for portable third-party packages | Usually commit or restore reproducibly | Plugin discovery expects the standard location and `plugin.cfg` |

The distinction matters in Git. Godot's version-control documentation says to ignore `.godot/` for Godot 4.1 and later. The import guide separately says to commit `.import` files, and the Godot 4.4 UID design note says not to ignore `.uid` files. These categories look similar in a file browser but have opposite source-control rules.

---

## 3. What Changed with UIDs, and What Did Not

### The 4.4 change

Godot 4.0 introduced partial resource UIDs. Imported assets could store an identity in `.import`, and native `.tscn` and `.tres` files could store one in their headers, but scripts and shaders lacked a place to keep it. Godot 4.4 generalized UID coverage by adding adjacent `.uid` files for resource types that could not embed identity. The 4.4 UID article explains that serialized resource references can store a UID while retaining a human-readable `res://` path as a display value and fallback.

The current TSCN format reference shows the result. A scene has its own `uid` in the file header. An external dependency contains a resource UID, a path, and a scene-local ID. A subresource contains only a scene-local ID because it lives inside the owning file.

Godot continued extending the system after 4.4. Godot 4.5 added editor support for dropping preloaded resources into code as UIDs and expanded UID use for extracted imported meshes, materials, and animations, according to the Godot 4.5 beta 1 release notes. Godot 4.6 extended UID use to autoloads, according to the 4.6 development notes. This incremental rollout is why advice written for "Godot 4" can still be too broad.

### What a UID protects

The Godot 4.7 `ResourceUID` reference states that UIDs preserve references when resource files are moved or renamed. For UID-backed serialized dependencies, a new filesystem path can be resolved from the stable identity.

The path fallback still matters. When a file is moved externally, dependent scenes or resources may warn that the stored text path is stale even though the UID resolves correctly. Re-saving the dependents updates the path and removes the warning.

### What a UID does not protect

UIDs do not turn every string into a durable reference. A literal `load("res://old/path.tres")`, a custom JSON field containing a path, `FileAccess` logic, build scripts, and third-party configuration remain path-based unless they explicitly use or resolve UIDs. Godot 4.4 also changed `@export_file` values selected in the Inspector to UID references; the 4.3-to-4.4 migration guide warns that arrays can contain a mix of `uid://` and `res://` values. Godot 4.5 added `@export_file_path` for code that specifically needs a raw path.

Node paths inside a scene are another identity domain. A resource UID tracks a resource file, not every `NodePath` string inside scene logic or animation data. Godot 4.6 added scene node `unique_id` data to improve node tracking, as documented in the TSCN reference, but that should not be mistaken for blanket refactor safety.

### Moving is not copying

For an external move, move the base file and its companion `.import` or `.uid` file together. The UID remains the same because it is still the same logical resource. Godot's 4.4 article explicitly requires this for scripts and shaders, and a maintainer-authored proposal for a missing UID manual page generalizes the rule to both sidecar types.

For a copy, a new resource should receive a new UID. Copying a scene together with its embedded UID or copying a source together with its `.import`/`.uid` sidecar creates duplicate identities. The editor's own duplicate operation is safer because it assigns a distinct identity. If copying an imported asset or script externally to create a new resource, omit the sidecar and allow Godot to generate a new one. Native `.tscn` and `.tres` copies need extra care because their UID is embedded.

---

## 4. The Documentation Contradiction on File Moves

The current Godot 4.7 filesystem guide still says to perform every move, delete, and rename in the FileSystem dock and to "never" move assets outside Godot. That advice reflects the old path-only failure mode. The newer UID design explicitly says support for external moves was a priority and explains how to perform them.

The best reconciled rule is:

1. **Use the FileSystem dock** for routine refactors and all duplications. It can inspect dependencies, update editor-managed references, and assign fresh UIDs to copies.
2. **External moves are supported** for UID-backed resources when the source and sidecar move as a unit. Expect to re-save dependents so their path fallbacks are current.
3. **External moves remain unsafe** for literal paths and custom path-bearing data. Search code and configuration for the old `res://` prefix.
4. **Use version control** before large reorganizations. UID support reduces breakage; it does not eliminate editor bugs, duplicate-identity mistakes, or path literals.

This is not merely a style preference. It is an example of the manual lagging behind an engine subsystem that changed in stages.

---

## 5. Scenes Do Not Mean "Everything Is Baked into One File"

A scene saved to disk is a `PackedScene`, which is itself a `Resource`. The Godot resources guide distinguishes two storage choices:

1. **Built-in resources** are serialized inside a `.tscn` or `.scn` file.
2. **External resources** are stored as independent files and referenced by the scene.

Scenes can also instance other scenes. A player scene can therefore reference a player script, external textures, an external data resource, and a separately instanced weapon scene while embedding a collision shape and a one-off material as subresources. The folder structure is not a serialization boundary; ownership and resource references are.

That produces a practical placement rule:

1. Keep a one-off resource **built into its scene** when it is private, small, and edited with the scene.
2. Save a resource **externally** when it is reused, independently edited, replaced by a pipeline, or likely to create conflicts inside a large scene file.
3. Keep an external resource **near its owning scene** when only that feature uses it.
4. **Promote it to the nearest meaningful shared folder** only after more than one feature owns the dependency.

This is partly a workflow inference from Godot's serialization model, not an engine rule. It minimizes needless files for private details while preserving reuse and reviewability where those matter.

### Imported 3D scenes need a source-versus-wrapper distinction

Imported `.glb`, `.gltf`, `.fbx`, and `.blend` content is generated from a source file and can be replaced on reimport. The Godot 4.7 import-configuration guide says direct manual modification of the imported scene is not normally possible because reimport replaces it. Godot provides import settings, import scripts, extracted external resources, and inherited scenes for local customization.

A maintainable character folder may therefore contain both the import source and a Godot-owned wrapper or inherited scene:

```
characters/player/
  player.glb
  player.glb.import
  player_model_inherited.tscn
  player.tscn
  player.gd
  player.gd.uid
  materials/
  audio/
```

`player.glb` is the DCC pipeline boundary; `player_model_inherited.tscn` preserves overrides; `player.tscn` composes the model with gameplay nodes and logic. They serve different ownership roles even though they describe one character.

---

## 6. The Organization Patterns That Actually Make Sense

### Type-first

```
assets/textures/
assets/audio/
scenes/
scripts/
```

This works mechanically and can be comfortable for small tutorials or discipline-based teams. Its cost is that one gameplay feature is scattered across several distant trees, and deleting or moving a feature requires finding its pieces everywhere. UIDs make the references more resilient but do not remove that navigation and ownership cost.

### Feature-first

```
characters/player/
characters/enemies/slime/
levels/forest/
ui/inventory/
```

Each folder contains the feature's scene, script, private art, audio, and data. This matches the official best-practices recommendation to group assets close to scenes. It also makes a feature easier to move, delete, test, or transfer as a unit.

### Hybrid feature-first, shared-by-evidence

This is the strongest default for most production projects. Features own their private dependencies; shared systems and assets have explicit homes. It avoids both extremes: a global texture warehouse and hundreds of duplicated copies hidden in feature folders.

For a large team, folder boundaries may also encode dependency direction. A contemporary GDQuest case study of a roughly 30-person Godot project describes separate reusable add-ons, game systems, UI, and content, with dependencies allowed in one direction. That is a useful scaling pattern, not a universal Godot standard; the same source warns that its overhead is unnecessary for many solo and small-team projects.

### There is no single community consensus, and that's worth saying plainly

Unlike a language with one dominant style guide, Godot's community visibly disagrees on this question in real time. A representative Godot Forum thread from a developer building a large 4.5 project shows them asking an LLM for a folder structure and then asking the forum to sanity-check it — precisely because no canonical answer exists to check it against. Community-maintained starter templates split the same way this report does: some (`theowiik/godot-template`) default to a type-first top level (`assets/`, `objects/`, `scenes/`, `scripts/`) with the same naming conventions described above; others build their entire pitch around project organization and coding standards as the main deliverable (`SamuelAsherRivello/godot-project-template`). A third independent source — a community-authored architecture guide explicitly benchmarked against the official manual and against discussions with other experienced Godot developers — converges on a `src/` source-code folder plus an `addons/` folder for third-party code and assets, but explicitly flags that separating source from scenes "probably won't confer you any benefits if you don't use an IDE," which is a genuinely different tradeoff calculus than the one in this report's feature-colocation default. Treat any single proposed structure, including the one in Section 7, as a starting point to adapt — not a spec.

### Root node naming inside scenes

Naming conventions converge more tightly than folder structure does, across the templates surveyed: directories and file names in `snake_case` (already covered in Section 1), but the **root node inside a scene** is conventionally named in `PascalCase` — `Player`, `MainMenu`, `GameLevel` — matching the class-like role that root node plays as the entry point for the scene's behavior. This is a naming convention rather than an engine requirement, but it is one of the few points in this whole topic where independent sources agree without qualification.

---

## 7. Recommended Reference Layout

The following layout deliberately separates the repository root from the Godot project root. Projects that do not need repository-level tooling can place `project.godot` at the repository root and keep the inner structure unchanged.

```
repository/
  README.md
  docs/                         # outside res://; Godot never scans it
  pipeline_tools/               # DCC/build scripts not used as Godot resources
  builds/                       # exported artifacts, ignored by Git

  game/                         # Godot project root = res://
    project.godot
    export_presets.cfg

    app/
      main.tscn
      main.gd

    content/
      characters/
        player/
          player.tscn
          player.gd
          player.gd.uid
          player.glb
          player.glb.import
          materials/
          audio/
        enemies/
          slime/
      worlds/
        forest/
          forest.tscn
          tileset.tres
          art/
          audio/

    systems/
      combat/
      dialogue/
      save/

    ui/
      inventory/
      menus/

    shared/
      audio/
      fonts/
      materials/
      shaders/
      data/

    addons/
      plugin_or_portable_package/
        plugin.cfg

    tests/
```

The directory names are not sacred. The placement rules are more important:

1. If only one scene or feature uses it, place it with that feature.
2. If several related features use it, move it to their nearest common parent.
3. If unrelated features use it, place it in `shared/` or a named system.
4. If it should work across projects, package it under `addons/` with no dependency on game-specific content.
5. If Godot should never load or export it, keep it outside the project root; use `.gdignore` only when outside placement is impractical.

The plugin documentation specifies `addons/plugin_name` as the standard editor-plugin path. The project-organization guide also suggests keeping third-party resources under `addons/` in general, while explicitly allowing feature-specific third-party assets to live with the feature they serve.

---

## 8. Source Control and Refactoring Checklist

### Commit

1. `project.godot`
2. `.tscn` and `.tres` sources; prefer these text forms to `.scn` and `.res` when collaboration and diffs matter
3. Gameplay scripts, shaders, source images, audio, models, fonts, and data
4. Every generated `.import` sidecar
5. Every generated `.uid` sidecar
6. `export_presets.cfg` for Godot 4.1 and later
7. `.gitattributes`, including Git LFS rules for large binary formats where appropriate

### Ignore

1. `.godot/`, including `imported/`, caches, and `uid_cache.bin`
2. `*.translation` as recommended by the current version-control guide
3. Exported builds and local IDE/build output

The export documentation says `export_presets.cfg` is safe to commit in modern Godot, while sensitive export credentials live under `.godot/export_credentials.cfg`, which is covered by ignoring `.godot/`.

### Before a large reorganization

1. Start from a clean commit and make the move its own reviewable change.
2. If upgrading an older project to 4.4+, let Godot add missing UID references and re-save scenes/resources before reorganizing. The 4.4 UID article recommends doing this in one pass to avoid later random diffs.
3. Prefer the FileSystem dock for the first structural move, especially when duplicating rather than moving.
4. If using Git, an IDE, or the OS for a move, move the base file and its `.import` or `.uid` companion together.
5. Search the repository for the old `res://` prefix and inspect custom configuration, JSON, localization, `FileAccess` code, and tool scripts.
6. Open and re-save dependent scenes/resources so UID-resolved references receive the new display/fallback path.
7. Run the game, import, and export from a clean checkout where `.godot/` must regenerate. A clean clone is the strongest test that all identity and import metadata were committed.

---

## 9. Stale or Misleading Advice, Corrected

| Claim | Current assessment |
|---|---|
| "Godot has no metadata." | Misleading after 4.4. It has no Unity-style universal metadata database, but `.import`, `.uid`, embedded UIDs, and generated caches are real metadata. |
| "Put everything under `Assets/`." | Optional and usually redundant. `res://` already is the asset root. |
| "Organize by file type." | Mechanically valid, but the official maintainability recommendation is to group dependencies near scenes. |
| "Everything belonging to a scene is baked into `.tscn`." | False. A scene may contain built-in resources, external resources, and instances of other scenes. |
| "Never move files outside Godot." | Too absolute for 4.4+. External moves can preserve UID-backed references if companion files move too, but the editor remains the safest default and literal paths still require repair. |
| "Ignore `.import` and `.uid`; Godot will regenerate them." | Wrong for teams. Regeneration can change identity or import behavior. Commit both. |
| "Commit `.godot/uid_cache.bin` so UIDs work on another machine." | Wrong. Official guidance is to ignore `.godot/`; durable identity is carried by embedded UIDs and adjacent sidecars. |
| "UIDs make paths irrelevant." | False. Paths remain UI/fallback data, and many code/config strings remain literal paths unless deliberately expressed as UIDs. |
| "Copy the sidecar whenever you copy the file." | Wrong. Move the sidecar for the same resource; do not copy it when creating a distinct resource with a new identity. |

---

## Conclusion

Godot's answer is not "choose any folders and nothing matters." It is:

1. The engine does not impose a canonical content hierarchy.
2. The official human convention is scene-local or feature-local organization.
3. The best production default is feature-first with narrowly defined shared and system folders.
4. Imported sources, native resources, built-in subresources, and generated caches have different ownership rules.
5. Modern UIDs make reorganizing safer, but only if `.uid` and `.import` sidecars are committed and moved correctly, and only for references that actually use the UID system.

**In one sentence:** organize around ownership and dependency locality, then obey the metadata mechanics that keep those dependencies intact.

---

## Material Limitations and Disagreements

1. Godot's documentation is internally inconsistent about external file moves. The 4.7 filesystem page preserves a blanket pre-UID warning, while the 4.4 UID design article and later maintainer documentation proposal explicitly support paired external moves. This report treats editor moves as the safest default and paired external moves as supported but conditional.
2. The 4.4 UID article displays an age warning. Its core behavior is corroborated by the current 4.7 `ResourceUID` and TSCN references, the current migration guide, and subsequent 4.5/4.6 release notes.
3. The recommended directory tree is a synthesis of official mechanics and maintainability guidance. It is not a mandatory Godot standard.
4. Open engine bugs can still affect UID caches or editor refactors in particular releases. Version control and clean-clone testing remain necessary even when the documented workflow is followed.

---

## Sources

Official Godot documentation and release materials are primary. The GDQuest case study is included only as a labeled example of large-team convention.

- Maintenance release: Godot 4.7.2. Godot Engine; Thaddeus Crews. August 18, 2026.
- Project organization. Godot Engine documentation. Godot 4.7.
- File paths in Godot projects. Godot Engine documentation. Godot 4.7.
- Import process. Godot Engine documentation. Godot 4.7.
- Version control systems. Godot Engine documentation. Godot 4.7.
- UID changes coming to Godot 4.4. Godot Engine; Hugo Locurcio. January 15, 2025.
- ResourceUID. Godot Engine documentation. Godot 4.7.
- TSCN file format. Godot Engine documentation. Godot 4.7.
- Resources. Godot Engine documentation. Godot 4.7.
- Import configuration. Godot Engine documentation. Godot 4.7.
- File system. Godot Engine documentation. Godot 4.7.
- Add manual page about UID, issue 11216. Godot documentation repository; KoBeWi. August 19, 2025.
- Upgrading from Godot 4.3 to Godot 4.4. Godot Engine documentation. Godot 4.7 migration guide.
- Godot 4.5 beta 1. Godot Engine; Thaddeus Crews. June 18, 2025.
- Godot 4.6 dev 4. Godot Engine; Thaddeus Crews. November 14, 2025.
- Making plugins. Godot Engine documentation. Godot 4.7.
- Exporting projects. Godot Engine documentation. Godot 4.7.
- Modular Game Architecture. GDQuest; Nathan Lovato with Ricard Pillosu. Updated June 15, 2026.
- Godot 4.4 Added .uid Files Everywhere. Here's What They Actually Do. DEV Community; Ziva. April 20, 2026.
- Folder structure for large game in Godot 4.5. Godot Forum. August 11, 2025.
- godot-template. GitHub; theowiik.
- godot-project-template. GitHub; Samuel Asher Rivello.
- godot-architecture-organization-advice. GitHub; abmarnie.
