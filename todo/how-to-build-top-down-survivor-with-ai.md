# How To Build The Top-Down Survivor Game With AI Assistance

This guide explains how to recreate the small Unity 2D top-down survivor game we built with AI assistance. It is written for someone who is new to both Unity and AI coding assistants.

The game you will build:

- A player moves with WASD or arrow keys.
- The player aims with the mouse.
- The player shoots projectiles.
- One enemy chases the player.
- Shooting the enemy destroys it and increases the score.
- A new enemy appears after the old one is destroyed.
- If the enemy touches the player, the game shows `Game Over` and freezes.

## What You Need

- Unity Hub installed.
- A Unity 2D project.
- An AI assistant such as Codex, ChatGPT, Claude, or another coding assistant.
- Basic ability to copy text from the AI and paste it into `.cs` script files.

You do not need to know C# before starting. Your job is to set up the Unity objects, ask the AI for small scripts one at a time, attach the scripts in Unity, and test the game after each step.

## Important Rule

Do not ask the AI to create Unity scenes, prefabs, or `.asset` files.

Use AI for scripts only. You will create and connect GameObjects, prefabs, tags, colliders, and Inspector fields yourself inside the Unity Editor.

This keeps the project safer because Unity scene and prefab files are easy to break when edited as raw text.

## Step 1: Create The Unity Project

1. Open Unity Hub.
2. Click **New Project**.
3. Choose **2D**.
4. Name the project something like `TopDownSurvivor`.
5. Click **Create Project**.

When Unity opens, save the scene:

1. Go to **File > Save As**.
2. Name it `MainScene`.
3. Save it inside the `Assets` folder.

## Step 2: Create Folders

In the Project window:

1. Right-click inside `Assets`.
2. Choose **Create > Folder**.
3. Name it `Scripts`.
4. Create another folder named `Prefabs`.

You will put C# files in `Assets/Scripts` and reusable objects in `Assets/Prefabs`.

## Step 3: Create The Player

1. In the Hierarchy, right-click.
2. Choose **2D Object > Sprites > Square**.
3. Rename it `Player`.
4. Select `Player`.
5. In the Inspector, click **Add Component**.
6. Add `Rigidbody2D`.
7. Set `Gravity Scale` to `0`.
8. Click **Add Component** again.
9. Add `Box Collider 2D`.

Set the Player tag:

1. Select `Player`.
2. At the top of the Inspector, open the **Tag** dropdown.
3. If `Player` exists, select it.
4. If not, choose **Add Tag...**, add `Player`, then return to the Player and select the tag.

## Step 4: Create The Camera Setup

Unity usually creates a Main Camera automatically.

1. Select `Main Camera`.
2. Make sure its tag is `MainCamera`.
3. Set its position to something like:

```text
X: 0
Y: 0
Z: -10
```

4. Make sure Projection is `Orthographic`.
5. Adjust `Size` until the play area looks comfortable.

## Step 5: Ask AI For Player Movement

Ask the AI:

```text
Unity 2D project, top-down view. I have a Player GameObject with a Rigidbody2D gravity scale 0 and a Box Collider 2D. Write a single C# MonoBehaviour PlayerMovement.cs that moves the player with WASD/arrow keys at a configurable speed, using Rigidbody2D velocity in FixedUpdate. Clamp the player so it cannot leave the camera view. Do not create or modify any other script. Do not generate prefabs, scenes, or .asset files. Output only the one script.
```

Create the script:

1. In `Assets/Scripts`, right-click.
2. Choose **Create > C# Script**.
3. Name it `PlayerMovement`.
4. Open it.
5. Replace everything with the AI's code.
6. Save the file.

Attach it:

1. Select `Player`.
2. Click **Add Component**.
3. Add `PlayerMovement`.
4. Set `Move Speed` to `5`.

Test it:

1. Press Play.
2. Move with WASD and arrow keys.
3. Make sure the player stops when keys are released.
4. Make sure the player cannot leave the screen.

If the AI uses `linearVelocity` and Unity gives an error, ask the AI to change it to `velocity`.

## Step 6: Ask AI For Player Aim

Ask the AI:

```text
Same Unity 2D top-down project. The Player already has a PlayerMovement script. Write a single C# MonoBehaviour PlayerAim.cs that smoothly rotates the player to face the mouse cursor, with no jitter when the mouse is still. Do not modify PlayerMovement or any other script. No prefabs, scenes, or .asset files. Output only the one script.
```

Create `PlayerAim.cs` in `Assets/Scripts`, paste the AI code, and save it.

Attach it:

1. Select `Player`.
2. Click **Add Component**.
3. Add `PlayerAim`.
4. Set `Rotation Speed` to something like `720`.

Test it:

1. Press Play.
2. Move the mouse.
3. Confirm the player rotates toward the cursor.
4. Confirm the player does not keep rotating just because you are moving with WASD.

If the player rotates when the mouse is not moving, tell the AI:

```text
The player autorotates when moving, even when the mouse is not moving. Update PlayerAim.cs so movement alone does not change the rotation.
```

## Step 7: Create The Projectile Prefab

1. In the Hierarchy, right-click.
2. Choose **2D Object > Sprites > Square**.
3. Rename it `Projectile`.
4. Scale it smaller, for example:

```text
X: 0.2
Y: 0.2
Z: 1
```

5. Add `Rigidbody2D`.
6. Set `Gravity Scale` to `0`.
7. Add `Box Collider 2D`.
8. Check **Is Trigger** on the Box Collider 2D.
9. Set the tag to `Projectile`. Create the tag if needed.

Make it a prefab:

1. Drag `Projectile` from the Hierarchy into `Assets/Prefabs`.
2. Delete the `Projectile` object from the Hierarchy after the prefab is created.

## Step 8: Ask AI For Shooting

Ask the AI:

```text
Same project. Write two C# scripts. (1) PlayerShoot.cs: on left mouse click, instantiate a projectile public GameObject projectilePrefab at the player's position, moving in the player's current facing direction, at a configurable speed public float projectileSpeed default 10 with a configurable fire rate public float fireRate shots per second default 5. (2) Projectile.cs: moves the projectile forward and destroys it after a configurable lifetime public float lifetime default 2. I will create the projectile prefab and assign it in the Editor. Do not modify other scripts. No prefab/scene/.asset authoring. Output only the two scripts.
```

Create both scripts in `Assets/Scripts`:

- `PlayerShoot.cs`
- `Projectile.cs`

Attach them:

1. Select `Player`.
2. Add `PlayerShoot`.
3. Drag the `Projectile` prefab from `Assets/Prefabs` into the `Projectile Prefab` field.
4. Select the `Projectile` prefab.
5. Add the `Projectile` script to the prefab.

Test it:

1. Press Play.
2. Move the mouse to aim.
3. Hold or click the left mouse button.
4. Confirm projectiles fire in the facing direction.
5. Confirm projectiles disappear after a short time.

## Step 9: Create The Enemy Prefab

1. In the Hierarchy, right-click.
2. Choose **2D Object > Sprites > Circle** or **Square**.
3. Rename it `Enemy`.
4. Add `Rigidbody2D`.
5. Set `Gravity Scale` to `0`.
6. Add `Box Collider 2D`.
7. Set the tag to `Enemy`. Create the tag if needed.

Make it a prefab:

1. Drag `Enemy` from the Hierarchy into `Assets/Prefabs`.
2. Delete the `Enemy` object from the Hierarchy after the prefab is created.

## Step 10: Ask AI For Enemy Chase

Ask the AI:

```text
Same project. Write a single C# MonoBehaviour EnemyChase.cs that moves the enemy smoothly toward the current position of the object tagged Player at a configurable speed public float chaseSpeed default 3. Do not modify other scripts. No prefab/scene/.asset authoring. Output only the one script.
```

Create `EnemyChase.cs`, paste the code, and save it.

Attach it:

1. Select the `Enemy` prefab in `Assets/Prefabs`.
2. Click **Add Component**.
3. Add `EnemyChase`.
4. Set `Chase Speed` to `3`.

## Step 11: Ask AI For Enemy Health And Spawning

Ask the AI:

```text
Same project. Write two C# scripts. (1) EnemyHealth.cs: when the enemy collides with an object tagged Projectile, destroy both the enemy and the projectile. (2) EnemySpawner.cs: spawns one enemy public GameObject enemyPrefab at a random screen-edge position, and spawns a new one whenever the current enemy is destroyed, keeping exactly one enemy alive at a time. I will assign prefabs in the Editor. Do not modify unrelated scripts. No prefab/scene/.asset authoring. Output only the two scripts.
```

Create both scripts:

- `EnemyHealth.cs`
- `EnemySpawner.cs`

Attach `EnemyHealth`:

1. Select the `Enemy` prefab.
2. Add `EnemyHealth`.

Attach `EnemySpawner`:

1. In the Hierarchy, right-click.
2. Choose **Create Empty**.
3. Rename it `EnemySpawner`.
4. Add the `EnemySpawner` script.
5. Drag the `Enemy` prefab into the `Enemy Prefab` field.

Test it:

1. Press Play.
2. Confirm one enemy appears.
3. Shoot the enemy.
4. Confirm the enemy and projectile are destroyed.
5. Confirm a new enemy appears about 1 second later.

## Step 12: Create The Score Text

1. In the Hierarchy, right-click.
2. Choose **UI > Text - TextMeshPro**.
3. If Unity asks to import TextMeshPro essentials, click **Import TMP Essentials**.
4. Rename the text object `ScoreText`.
5. Set its text to:

```text
Score: 0
```

6. Place it near the top-left of the screen using the Rect Transform.

## Step 13: Ask AI For ScoreManager

Ask the AI:

```text
Same project. Write a single C# MonoBehaviour ScoreManager.cs that holds an int score, exposes a public method AddKill() that increments it by 1, and displays the score via a public reference to a TextMeshProUGUI field. Then tell me the exact one line to add to EnemyHealth so it reports a kill to ScoreManager. I will wire the UI reference in the Editor. Do not restructure other scripts. No scene/.asset authoring beyond what I do in the Editor. Output only the one script plus the single integration line.
```

Create `ScoreManager.cs`, paste the code, and save it.

Attach it:

1. In the Hierarchy, right-click.
2. Choose **Create Empty**.
3. Rename it `ScoreManager`.
4. Add the `ScoreManager` script.
5. Drag `ScoreText` into the `Score Text` field.

Update `EnemyHealth.cs`:

Add this line before `Destroy(gameObject);` when a projectile kills the enemy:

```csharp
FindObjectOfType<ScoreManager>()?.AddKill();
```

Test it:

1. Press Play.
2. Shoot an enemy.
3. Confirm the score changes from `Score: 0` to `Score: 1`.
4. Shoot another enemy.
5. Confirm the score increases only once per kill.

## Step 14: Add Game Over Without A New Script

You can handle Game Over by modifying existing scripts.

Ask the AI:

```text
I do not want to add a new script. Modify the existing ScoreManager.cs and EnemyHealth.cs so that when an enemy touches the player, the score text changes to Game Over and the game freezes using Time.timeScale = 0. Keep the existing score and projectile kill behavior.
```

The idea is:

- `ScoreManager` gets a public method named `ShowGameOver()`.
- `EnemyHealth` calls `FindObjectOfType<ScoreManager>()?.ShowGameOver();` when it touches an object tagged `Player`.

Important Unity setup:

- Player must have a `Box Collider 2D` or another `Collider2D`.
- Enemy must have a `Collider2D`.
- At least one of them must have a `Rigidbody2D`.
- Player tag must be exactly `Player`.
- Enemy tag must be exactly `Enemy`.

Test it:

1. Press Play.
2. Let the enemy touch the player.
3. Confirm the text changes to `Game Over`.
4. Confirm the game freezes.

If nothing happens, check whether the Player has a collider. In our build, Game Over did not work until we added a `Box Collider 2D` to the Player.

## Step 15: The Final Attachment Map

Use this checklist if something is not working.

### Player GameObject

- Tag: `Player`
- `Rigidbody2D`
- Gravity Scale: `0`
- `Box Collider 2D`
- `PlayerMovement`
- `PlayerAim`
- `PlayerShoot`
- `Projectile Prefab` field assigned in `PlayerShoot`

### Projectile Prefab

- Tag: `Projectile`
- `Rigidbody2D`
- Gravity Scale: `0`
- `Box Collider 2D`
- `Is Trigger`: checked
- `Projectile`

### Enemy Prefab

- Tag: `Enemy`
- `Rigidbody2D`
- Gravity Scale: `0`
- `Box Collider 2D`
- `EnemyChase`
- `EnemyHealth`

### EnemySpawner GameObject

- Empty GameObject in the scene
- `EnemySpawner`
- `Enemy Prefab` field assigned

### ScoreManager GameObject

- Empty GameObject in the scene
- `ScoreManager`
- `Score Text` field assigned to the TextMeshProUGUI score label

## Step 16: How To Work With The AI

Use AI in small steps. Do not ask it to build the whole game at once.

Good pattern:

1. Ask for one script or one small feature.
2. Paste the code into Unity.
3. Attach the script yourself.
4. Press Play.
5. Describe exactly what went wrong.
6. Ask the AI for a focused fix.

Example:

```text
The player leaves the screen when I keep pressing movement keys. Update only PlayerMovement.cs so the player stays inside the camera bounds.
```

Another example:

```text
The enemy touches the player but Game Over does not happen. The enemy has a Box Collider 2D, but the player does not. What should I add?
```

## Step 17: What We Learned From Testing

These were the important human play-test catches:

- The first movement script used `linearVelocity`, but this Unity version needed `velocity`.
- The player could leave the screen, so we added camera bounds.
- The aim script could rotate while moving even when the mouse was still, so we changed the aim behavior.
- Game Over did not work until the Player had a collider.
- The score and Game Over behavior needed to be connected through `ScoreManager`.

These are exactly the kinds of issues AI may not catch by itself. The AI can write code, but the human must play the game and decide whether it feels right.

## Step 18: Create A Verified Skill Note

After the game works, save one reusable thing you learned as a markdown note.

For this project, we made:

```text
unity-2d-bounded-player-movement.md
```

That note includes:

- The final working movement pattern.
- The required Unity setup.
- The tested behavior.
- What broke.
- What we fixed.
- What we did not test.

This is useful because the next time you make a similar Unity 2D game, you do not have to start from scratch. You can reuse the verified recipe.

## Done Condition

You are done when:

- Player moves and stays on screen.
- Player aims with the mouse.
- Player shoots projectiles.
- Enemy chases the player.
- Projectile destroys enemy.
- Score increases by 1 per kill.
- A new enemy spawns after the old one dies.
- Enemy touching player shows `Game Over`.
- The game freezes on Game Over.
- You have written down at least one reusable verified note from the process.
