# UNITY.md — environment pin + script conventions

The missing control. "Identical prompts" only isolates the agent if the *environment* is identical too — otherwise each agent's training priors (Unity version, input system, API names) become hidden variables logged as agent differences. Both builders give their agent this file as context before Increment 1. Lean on purpose: only what the pilot needs. Design doctrine waits for the tooling-gap list.

## Environment (pinned)

| What | Pin |
|---|---|
| Unity version | **Unity 6 LTS (6000.0.x)** — record the exact patch in the harness README; both builders byte-identical |
| Template | 2D (built-in or URP — whichever the harness uses; both builders identical) |
| Packages | Whatever ships with the template + TextMeshPro (via uGUI) + the pre-installed libraries below. **Agents never add packages or edit `Packages/manifest.json`** — the human installs everything in the harness before cloning. |
| Active Input Handling | **Both** (Project Settings → Player) — so either input path compiles |

## Unity 6 API pins (agents get these wrong most)

Training data skews old. These renames are the most likely first-paste failures:

| Old (pre-Unity 6) | Unity 6 | Note |
|---|---|---|
| `rigidbody2D.velocity` | `rigidbody2D.linearVelocity` | Increment 1 hits this immediately |
| `rigidbody2D.drag` / `.angularDrag` | `.linearDamping` / `.angularDamping` | |
| `FindObjectOfType<T>()` | `FindFirstObjectByType<T>()` | deprecated, warns |
| `FindObjectsOfType<T>()` | `FindObjectsByType<T>(FindObjectsSortMode.None)` | |

An agent emitting the old form is a **logged finding** (feedback log → first-try quality), then corrected.

## Pre-installed libraries (in the harness — agents may use, never install)

Installed by the human in the Editor **before** the harness is cloned, so both builders are byte-identical. Picked for one thing: agents write their APIs correctly unprompted, so juice costs one line instead of a round-trip.

| Library | What | Why it's here |
|---|---|---|
| **DOTween (free, Asset Store)** | One-line tweens: `transform.DOPunchScale(...)`, `transform.DOShakePosition(...)` | The cheapest path from "compiles" to "feels right" — hit reactions, kill pops, smooth aim. Both agents know `DG.Tweening` cold from training data. Human runs the DOTween Utility Panel setup once, in the Editor. |
| **Cinemachine (ships with Unity 6, CM 3.x)** | Camera + `CinemachineImpulse` for screen shake on shoot/kill | Screen shake is the highest-value juice per line of code. **API pin:** CM3 renamed things — namespace is `Unity.Cinemachine`, `CinemachineVirtualCamera` → `CinemachineCamera`. Agents trained on CM2 will get this wrong; that's a logged finding, then corrected. |

Already built in — **don't let the agent add a library for these**:

- **TextMeshPro** (via uGUI) — score UI.
- **`UnityEngine.Pool.ObjectPool<T>`** — if pooling ever comes up (it shouldn't in week 1; one enemy, short-lived projectiles).
- **ParticleSystem** — muzzle flash, death puffs. No asset needed for primitive-shape particles.

Considered, not installed: **Feel/MMFeedbacks** (the gold standard for juice, but paid — revisit when the tooling budget exists), **PrimeTween** (technically better than DOTween, but thinner training data = more agent round-trips, which is the wrong trade for this pilot), **A\* Pathfinding Project** (straight-line chase needs nothing).

Same membrane as always: agents *reference* these from C#; wiring a Cinemachine camera or impulse listener happens in the Editor, by the human.

## Input (deliberately not pinned — but with a default)

Legacy Input Manager (`Input.GetAxis`, `Input.GetKey`) and the new Input System are **both allowed**. Which one the agent reaches for unprompted is a finding, not a bug — log it in the feedback log (Input path field).

**Default: legacy Input Manager.** The unpinned choice is an observation protocol, not a requirement to debug. The moment input costs you a round-trip — doesn't compile, agent asks which system, keys don't respond — tell the agent: *"Use the legacy Input Manager (`Input.GetAxis` / `Input.GetKey`), not the Input System package."* Log the original choice and the fallback, then move on. Legacy is the default because it needs zero package setup and works under Active Input Handling = Both. A builder who's never fought Unity's input stack should never spend more than one round-trip here — the pilot is measuring feel, not input-system archaeology.

## Script conventions

1. **The prompt wins.** Where a pilot prompt says `public float moveSpeed`, write exactly that — do not "improve" it to `[SerializeField] private`. Conventions below apply only where the prompt is silent.
2. One class per file; filename = class name.
3. Physics (velocity, forces, movement of Rigidbody2D) in `FixedUpdate`; input capture and rotation-to-mouse in `Update`.
4. Cache component references in `Awake`; never `GetComponent` / `GameObject.Find` per frame.
5. Use `CompareTag("X")`, not `tag == "X"`.
6. Null-check Editor-wired references (`projectilePrefab`, UI fields) with a clear error, don't NPE silently.
7. No namespaces, no singletons, no events/managers/architecture the prompt didn't ask for. Scope creep is a logged membrane-pressure finding.
8. Scripts live in `Assets/Scripts/`. Agents don't create other folders.

## Membrane rules for script authoring (restated from AGENTS.md)

- Agent output is **`.cs` files only** — never `.meta`, `.prefab`, `.unity` scenes, ScriptableObject `.asset`, or `ProjectSettings/` edits as text.
- The human attaches components, assigns fields, sets tags, and wires UI **in the Editor**.
- If the agent offers to generate a prefab/scene "to save time," refuse and log it (feedback log → membrane pressure).
