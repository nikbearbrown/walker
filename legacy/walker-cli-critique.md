# Thoughts on the Unity/Unreal CLI + Walker

You asked for thoughts, so here's the honest version. The methodology is good. The product framing has three soft spots that will decide whether this becomes a tool or stays a very elaborate prompt.

## 1. "Unity *or* Unreal" is two products wearing one coat

Drop the "or" for now. Unity and Unreal don't share the constraint your whole methodology is built around. Unity's danger is `.meta` GUIDs and YAML scenes. Unreal's danger is **Blueprints** — binary visual-script assets that aren't text, aren't diffable, and aren't editable by any CLI or LLM at all — plus UBT modules and a C++ build graph. The "membrane between AI-safe text and human-only assets" sits in a completely different place in each engine. A tool that pretends to span both will be mediocre at each. Pick Unity, ship it end-to-end, *then* ask what survives the port. Unreal is a sequel, not a checkbox.

## 2. The core contradiction: a CLI that isn't allowed to touch files

Your strongest rule — "all moves happen inside the Unity Editor, never via filesystem" — directly contradicts the thing you said you want to build: "a CLI that programs Unity." If the rule is literally true, the CLI can never do the one operation (restructuring) you named as step one. So one of two things has to give, and *which one* is the actual product decision:

- **(a) The CLI is only an advisor.** It audits, generates manifests, writes CLAUDE.md, runs verification — and a human does every move by hand in the Editor. Safe, but it's a linter with good manners, not "programming Unity from a CLI."
- **(b) The CLI is GUID-aware and *does* the moves safely.** This is the interesting product, and it's achievable — see below.

Right now Walker assumes (a) but your stated vision is (b). Name which one you're building before writing another line of persona.

## 3. "Never move via filesystem" is a safe heuristic, not a law of physics

This matters enough to get precise about, because it's the crux of whether (b) is even possible. Unity resolves references by **GUID**, and the GUID lives in the `.meta` file, not in the path. Move `Foo.cs` **and** `Foo.cs.meta` together and every reference survives — the asset database just remaps GUID→new path on reimport. The damage in your Failure Mode #2 comes from moving the asset *without* its meta, or letting something regenerate a fresh meta. So:

- The Editor isn't magic. It's doing a GUID-preserving move you can replicate.
- The genuinely safe primitive already exists: **`AssetDatabase.MoveAsset()`**, callable from `Unity -batchmode -executeMethod`. That's a CLI driving Unity's own integrity guarantees — not a filesystem hack around them.
- So the move executor should generate a manifest (you already have `/movetable`) and *apply it through batchmode*, not through `mv`. That's your option (b), and it's safe by construction.

Reframing the rule from "never move outside the Editor" to **"never move without the GUID, and prefer AssetDatabase as the executor"** unlocks the actual tool without giving up the safety it's protecting.

## 4. Build on Unity's tooling, not beside it

Unity already ships headless batchmode, `AssetDatabase`, asmdef, and the Test Runner. There are also existing Unity MCP servers worth studying before you build. The defensible product is a thin, opinionated layer that *orchestrates Unity's own primitives* from a manifest — not a new engine for understanding Unity projects. Every line you write that re-derives what `AssetDatabase` already knows is a line that will drift out of sync with the next Unity version.

## 5. You've over-built the conductor and I can't see the orchestra

The persona, five phases, five capacities, seven failure modes, thirty-odd commands — it's genuinely sharp thinking, and the labor-separation table is the best artifact in the whole thing. But all of it is *prompt*. The product is four pieces of actual engineering:

1. **The indexer** (`unity_project_walker.py`) — the project map.
2. **The move executor** — manifest → `AssetDatabase.MoveAsset` via batchmode.
3. **The CLAUDE.md generator** — audit report → constitution.
4. **The verification engine** — golden-master / characterization tests + the report.

The hardest and most valuable of these is #4, and it's the least specified. Characterization tests for MonoBehaviour `Update()` ordering and coroutine timing are *the* hard problem in Unity refactoring — that's exactly why no AI can do it. If the verification engine works, the product works. The persona is decoration on top of that.

So the one question that decides everything: **what does the walker script actually do today, and has the full A→E loop ever run on one real legacy project?** If yes, lead with that case study — it's worth more than the entire landing page. If no, that's the next thing to build, and the prompt is premature.

## 6. The reframe I'd actually push: build around *the membrane*

Strip the five phases for a second and there's a cleaner spine underneath. Every game engine has a line between:

- the **text layer** — C#, asmdef, config — which is diffable, reviewable, and AI-safe, and
- the **asset layer** — scenes, prefabs, ScriptableObject `.asset` files, Blueprints — which is binary/serialized, reference-by-id, and Editor-only.

Your entire methodology is one rule applied repeatedly: *the AI works the text layer; the human (or the Editor, scripted) works the asset layer; the membrane between them is sacred.* That single idea generalizes to Unreal for free (the membrane just moves to Blueprints + modules), and it's a sharper pitch than "five phases and a boondoggle." The phases are *how* you respect the membrane. Lead with the membrane.

## 7. Be honest about the ceiling of "program Unity via CLI"

A CLI's natural domain is the text layer. It will never *author* a scene, wire a prefab, or write a valid binary `.asset` — you say so yourself in the "dangerous middle." So the durable, true product is **"AI-assisted C# and project-structure work for Unity, with a hard membrane protecting the asset layer"** — not "program your whole game from the terminal." Naming that ceiling out loud makes the tool more credible, not less. Overclaiming the asset layer is how you get a demo that detonates on someone's real project and kills the trust the whole thing runs on.

## 8. Smaller things

- **Staleness is a CI problem, not a discipline problem.** Failure Mode #7 (stale CLAUDE.md) won't be solved by willpower. The index and CLAUDE.md need a `walker verify --drift` that fails in CI when the map and the repo disagree. Make staleness *break the build*.
- **Four small tools, not one CLI.** Indexer, executor, generator, verifier — Unix them. A monolith called `walker` that does all four will be harder to trust and harder to test than four composable commands.
- **The persona and the tool are different deliverables.** Walker-the-prompt conducts; walker-the-CLI executes. Keep them in separate repos and don't let the prompt reference tool behavior that the tool doesn't actually have yet — that gap is its own Failure Mode #3.

## The one move I'd make next

Take one real, ugly, legacy Unity project and drive it A→E with whatever tooling exists today, by hand where the tool is missing. Write down every place you had to do something the tool couldn't. *That* list is your roadmap, and it'll be shorter and more honest than the command set you've already designed.
