# One-Week Gate Pilot — Codex vs Claude, One Game

## The experiment

Two builders. **Same game, same spec, same gate protocol, same prompts.** The only thing that varies is the AI coding agent: **Builder A uses Codex, Builder B uses Claude Code.**

What this isolates: where the produce → play → solidify → gate loop behaves differently across agents, and whether the gate methodology holds regardless of which agent is underneath.

What it does **not** buy: validation. n=2, one week, one game. It's a head-to-head feel test that surfaces *friction* and *agent differences*, not a benchmark. Treat conclusions as hypotheses.

## Governance — inherits SNICKERDOODLE

This pilot does not invent its own rules. It runs under the Reallocation Engine constitution (`SNICKERDOODLE.md`). The gate is just its principles in a game costume:

- **P1 — machines verify conformance, humans verify adequacy.** Agent code compiles and runs = conformance (machine-checkable). "Feels solid when played, not floaty/shaky" = adequacy (only the human, who can play, can clear it).
- **P2 — stored skills before ad-hoc code.** Reach for an existing skill/recipe before letting the agent reinvent it. Reinventing what a skill already does is a logged violation, not a neutral choice.
- **P4 — gates are hard stops** cleared by a named human and logged. "Looks good" is not a handoff condition; "solid when played, value locked" is.
- **P8 — trust is earned, not configured.** Lighter gates (silent mode) are *earned* by a VERIFIED skill + attestation, revoked by any change. Whether the builders earn it by Friday is a finding, not a setting.

## The mission (this is the real deliverable)

The game is the vehicle. The deliverable is **at least one VERIFIED, reusable skill** that the builders produce by working the agent — climbed through the recipe lifecycle and carrying an attestation:

```
DRAFT → SPECIFIED → RUNNABLE-SAMPLE → RUNNABLE-LIVE → VERIFIED
```

A skill does not count because it ran once. It counts when it has an attestation record (below) bound to its version. **Keep the skill agent-neutral** — a Unity recipe, not "Claude's recipe" or "Codex's recipe" — or skill production re-couples to the agent you're comparing.

## Controls (don't skip — they're what make the comparison mean anything)

1. **Identical prompts.** Both builders paste the *same* per-increment prompt block (below). Free-styled prompts measure prompting skill, not the agent. This is the whole ballgame.
2. **Identical "definition of solid."** Each gate has a shared pass condition (below). Otherwise two humans judging "solid" differently becomes a hidden variable.
3. **Matched-skill builders — both Unity-comfortable (confirmed).** Removes skill as a variable, so the comparison is genuinely Codex vs Claude. Note the consequence: with two experts you're testing whether the gates *keep good agents honest* (scope creep, membrane breaches, plausible-but-wrong feel waved through under speed) — not whether gates rescue a novice who can't tell solid from shaky. Don't let the debrief over-claim "gates help everyone" off a two-expert sample.
4. **Same engine setup.** Pinned in **`unity/UNITY.md`**: Unity 6 LTS (6000.0.x), same 2D template, same starting scene, Active Input Handling = Both. Both builders hand their agent `UNITY.md` as context before Increment 1 — otherwise agent training priors (old `Rigidbody2D.velocity` API, input-system choice) become hidden variables logged as agent differences. Only the agent differs.

## The game (shared spec)

**One-screen top-down survivor.** Six increments. **Each increment is a gate** — you do not start the next until the current one is *solid when played*, not when the agent emits plausible C#. The human plays; the agent can't. Source media is layer 2 (generate freely); **importing/wiring assets, prefabs, and scenes is Editor-only — the agent never authors `.prefab` or scene `.asset` files.**

Each increment below gives: the **paste prompt** (identical for both agents) and the **definition of solid** (the shared gate bar).

### Increment 1 — Move

```
Unity 2D project, top-down view. I have a Player GameObject with a Rigidbody2D (gravity scale 0). Write a single C# MonoBehaviour `PlayerMovement.cs` that moves the player with WASD/arrow keys at a configurable speed (public float moveSpeed, default 5), using Rigidbody2D velocity in FixedUpdate. Do not create or modify any other script. Do not generate prefabs, scenes, or .asset files — I will attach this component and set fields in the Unity Editor. Output only the one script.
```

**Solid when:** player moves all four directions, stops cleanly on key release, no drift, and moveSpeed tuned to a speed both builders agree feels controllable.

### Increment 2 — Aim

```
Same Unity 2D top-down project. The Player already has a PlayerMovement script. Write a single C# MonoBehaviour `PlayerAim.cs` that smoothly rotates the player to face the mouse cursor every frame, with no jitter when the mouse is still. Do not modify PlayerMovement or any other script. No prefabs, scenes, or .asset files. Output only the one script.
```

**Solid when:** player faces the cursor, tracks smoothly while moving, and shows no visible jitter at rest.

### Increment 3 — Shoot

```
Same project. Write two C# scripts. (1) `PlayerShoot.cs`: on left mouse click, instantiate a projectile (public GameObject projectilePrefab) at the player's position, moving in the player's current facing direction, at a configurable speed (public float projectileSpeed, default 10) with a configurable fire rate (public float fireRate, shots per second, default 5). (2) `Projectile.cs`: moves the projectile forward and destroys it after a configurable lifetime (public float lifetime, default 2). I will create the projectile prefab and assign it in the Editor. Do not modify other scripts. No prefab/scene/.asset authoring. Output only the two scripts.
```

**Solid when:** clicking fires in the aim direction, fireRate feels neither machine-gun nor sluggish, projectile speed reads well, and projectiles despawn.

### Increment 4 — Enemy chase

```
Same project. Write a single C# MonoBehaviour `EnemyChase.cs` that moves the enemy smoothly toward the current position of the object tagged "Player" at a configurable speed (public float chaseSpeed, default 3). Do not modify other scripts. No prefab/scene/.asset authoring. Output only the one script.
```

**Solid when:** enemy reaches the player on a smooth path, chaseSpeed is beatable but threatening, no stutter or jitter.

### Increment 5 — Kill + respawn

```
Same project. Write two C# scripts. (1) `EnemyHealth.cs`: when the enemy collides with an object tagged "Projectile", destroy both the enemy and the projectile. (2) `EnemySpawner.cs`: spawns one enemy (public GameObject enemyPrefab) at a random screen-edge position, and spawns a new one whenever the current enemy is destroyed, keeping exactly one enemy alive at a time. I will assign prefabs in the Editor. Do not modify unrelated scripts. No prefab/scene/.asset authoring. Output only the two scripts.
```

**Solid when:** projectile destroys the enemy on contact, exactly one enemy is alive at any moment, and a replacement spawns within ~1 second.

### Increment 6 — Score

```
Same project. Write a single C# MonoBehaviour `ScoreManager.cs` that holds an int score, exposes a public method AddKill() that increments it by 1, and displays the score via a public reference to a TextMeshProUGUI field. Then tell me the exact one line to add to EnemyHealth so it reports a kill to ScoreManager. I will wire the UI reference in the Editor. Do not restructure other scripts. No scene/.asset authoring beyond what I do in the Editor. Output only the one script plus the single integration line.
```

**Solid when:** score increments exactly once per kill and displays correctly on screen.

## Starter project skeleton (shared harness — build once, clone to both)

A reference *harness*, not a reference game. Identical Editor-side setup so the only variable is the agent's code. No imported *art* assets — primitives only, so the asset-import membrane stays out of week 1 entirely. Libraries are the one exception: the human pre-installs DOTween and Cinemachine per `unity/UNITY.md` (Editor-side, before cloning), so juice is one line away for both agents equally.

Environment pinned by `unity/UNITY.md` (Unity 6 LTS 6000.0.x — record the exact patch here when built; Active Input Handling = Both). Build one Unity project containing, and **nothing else**:

- A **Player** GameObject — a primitive square sprite, `Rigidbody2D` (gravity scale 0), tagged `Player`.
- An **Enemy** prefab shell — a primitive circle sprite, `Rigidbody2D`, `Collider2D`, tagged `Enemy`. No scripts.
- A **Projectile** prefab shell — a primitive capsule/small square, `Rigidbody2D`, `Collider2D` (trigger), tagged `Projectile`. No scripts.
- Tags configured: `Player`, `Enemy`, `Projectile`.
- One empty scene with the Player placed, a camera, and a TextMeshProUGUI score label (unwired).
- **Zero C# scripts.** The agents write every script from the six prompts.

Clone it byte-for-byte to both builders. Whatever's in the harness, neither agent authored — so it can't be the thing that differs. (No download of a reference *game* — a playable/source reference would let the agents copy known code, collapse "solid" into "matches the reference," and kill the moments where the human catches plausible-but-wrong by playing.)

## The gate protocol (each builder, every increment)

Walker's general gate doctrine is the rolling horizon in `core/gates.md` — plan three steps, step-gate each, fork-gate the horizon. **This pilot deliberately freezes the fork gates:** the six-increment path is fixed because the Codex-vs-Claude comparison requires identical paths. Only step gates run live here. That's an experimental control, not the doctrine.

1. **Paste the prompt** — verbatim, into your agent (Codex or Claude Code).
2. **Human plays** — run it in the Editor and play it. Non-delegable.
3. **Back and forth** — "too fast / too floaty / too shaky" → agent adjusts → play again, until it meets the definition of solid.
4. **Gate** — declare **solid / deferred / cut**. Only `solid` opens the next increment.

## Feedback log (one row per increment, per builder)

| Field | Capture |
|---|---|
| Agent | Codex / Claude Code |
| Increment | 1–6 |
| Round-trips to solid | how many paste→play cycles |
| First-try quality | did the first output run? compile? feel close? old-API misses (see UNITY.md pins)? |
| Input path chosen | which input system the agent reached for unprompted (legacy / new Input System) — finding, not bug. If it cost a round-trip, fall back to the default (legacy — see UNITY.md) and log both |
| What only playing revealed | the PA moments — the agent emitted plausible code that was wrong when played |
| Where the tooling couldn't keep up | anything done by hand because no tool did it |
| Membrane pressure | did the agent try to author a prefab/scene, or push you to? |
| Gate decision | solid / deferred / cut |
| Gate: helped or ceremony? | one word + why |

Daily: each builder leaves a one-line note — where they ended, what hurt.

## Attestation (SNICKERDOODLE format — the closing artifact per builder)

When a skill reaches VERIFIED, it carries this. The **Did not test** section is mandatory — an empty one is the new "it works," and it's exactly what catches an expert waving a shaky build through under speed.

```markdown
## Attestation
- Skill: <name> v<version>   (agent-neutral — a Unity recipe, not "Claude's"/"Codex's")
- By: <name> · <date> · Agent used to draft it: <Codex | Claude Code>

### Tested
| Ran | Saw | Expected |
|---|---|---|
| <command or play action> | <observed feel/result> | <definition of solid> |
| <at least one deliberate attempt to break it> | ... | ... |

### Did not test
- <honest list>

### Broke during testing, fixed
- <what failed, what changed, where>
```

## P8 — the earn-silent trial (run once the first skill hits VERIFIED)

This is the doctrine testing itself. P8: trust is earned, not configured — silent mode (no human play-gate) is *earned* by a VERIFIED skill + attestation, and revoked by any change.

**Trigger:** a builder's first skill reaches VERIFIED (attested, increment solid).

1. **Find an unchanged reuse.** Pick the next increment that reuses the same verified pattern *unchanged* (e.g. the movement recipe applied to a second moving object). If the recipe has to change to fit, silent is not legitimately earned — note that and stop. You've already found something: the pattern wasn't as reusable as it looked.
2. **Run it silent.** Accept conformance (compiles + runs) as the gate. Do **not** play-test for adequacy first. Advance as if trusted.
3. **Then play it.** Two outcomes, both findings:
   - **Holds** → trust transferred; the play-gate was safely removable for this pattern. Record what made it safe.
   - **Breaks** → silent let a regression through; conformance ≠ adequacy even for a verified pattern. Record exactly what playing caught that compiling didn't.
4. **Watch for the violation in the wild.** Log whether either agent or builder was tempted to declare silent on a recipe that had actually changed. That's the P8 failure mode live, and the most likely way "earned trust" rots in practice.

The question you're answering: does "trust is earned" survive contact, or does every reuse still need a human to play it? That answer is worth more than either finished game.

## End-of-week debrief — head to head

1. **Round-trips:** which agent needed fewer paste→play cycles per increment, and on which increments?
2. **Failure shape:** how did Codex's plausible-but-wrong differ from Claude's? (compile errors vs feel errors vs scope creep)
3. **Membrane discipline:** did either agent push harder to author prefabs/scenes or wander out of the one-script bound?
4. **Where the gate caught a real problem** the agent couldn't see — and was it the same increments for both agents? (same = it's the method; different = it's the agent)
5. **Where the gate was ceremony** — correct work slowed down. Same for both agents?
6. **Tooling-gap list:** everything either builder did by hand that a tool should have done. This is your CLI roadmap, written by users.

If questions 4 and 6 produce specific answers, the pilot worked — whether or not either game shipped.
