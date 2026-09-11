# Research Prompt: How Does Godot Want Scripts Written?

## Core Problem

Godot has an opinionated but under-enforced idea of "correct" GDScript. Unlike languages with a single dominant linter (Black for Python, gofmt for Go), Godot's conventions live in three places that don't always agree: the official style guide (aspirational, human-written), the built-in script editor's auto-formatting (partially enforces the guide), and the actual codebase idioms used in shipped Godot projects (signals, `@onready`, scene composition over inheritance). A model or developer asked to "write it the Godot way" needs to reconcile style (syntax, naming, layout) with architecture (how scripts should relate to nodes, scenes, and each other) — these are two different questions people conflate. This research prompt is built to separate them and produce code that is idiomatic in both senses, not just PEP-8-adjacent GDScript that ignores how Godot actually wants object communication structured.

---

## Part 1: Formatting and Naming Conventions (the PEP 8 layer)

GDScript's own style guide is explicitly modeled on Python's PEP 8, since the language borrows Python's indentation-based syntax. Since GDScript is close to Python, the guide is inspired by Python's PEP 8 programming style guide, and style guides aren't meant as hard rulebooks — when you can't apply a guideline, use your best judgment and prioritize consistency within your project or team over strict adherence. That caveat matters: a research/implementation prompt should treat these as strong defaults, not hard-fail lint rules.

Key conventions to encode:
- **File naming**: snake_case for file names; for named classes, the PascalCase class name converts to snake_case for the file (e.g., `class_name Weapon` → `weapon.gd`).
- **Naming by symbol type**: classes/nodes in PascalCase, functions/variables in snake_case, constants in CONSTANT_CASE, signals as snake_case verbs (past tense, e.g. `health_depleted`), private members prefixed with a single underscore.
- **Numeric literals**: use underscores for readability in large numbers (`1_234_567_890`), but skip them under ~1,000,000.
- **String quoting**: prefer double quotes; fall back to single quotes only to avoid escaping.
- **Statement layout**: one statement per line, blank line between function/class definitions, one blank line inside a function to separate logical sections, two indent levels for continuation lines (to visually distinguish them from a nested block).
- **Doc comments**: `##` (double-hash) for documentation comments that appear in the built-in docs panel, placed directly above the class or member they document.

```gdscript
class_name StateMachine
extends Node
## Hierarchical state machine for the player.
##
## Initializes states and delegates engine callbacks
## ([method Node._physics_process], [method Node._unhandled_input]) to the
## active state.

signal state_changed(previous: State, next: State)

@export var starting_state: State

var _current_state: State

@onready var _states: Array[State] = %States.get_children()


func _ready() -> void:
    _current_state = starting_state
    _current_state.enter()


func _physics_process(delta: float) -> void:
    _current_state.physics_update(delta)
```

Implementation note: GDScript's built-in script editor already applies many of these conventions by default, so a code-generation prompt should assume the target is "what the default editor formatting produces," not a from-scratch style invention. There's also a community formatter (`gdscript-formatter`, built on the Tree-Sitter GDScript parser) that aims to follow the official GDScript style guide and is a reasonable ground-truth to lint generated code against if you're automating this.

---

## Part 2: Static Typing — Optional but Increasingly the Norm

GDScript is gradually-typed: everything above works untyped, but Godot 4's idiomatic style leans hard into explicit types (`var health: int = 100`, `func take_damage(amount: int) -> void:`) because it unlocks editor autocomplete, catches errors before runtime, and measurably improves performance versus dynamic typing. A prompt/model should default to fully-typed signatures and typed arrays (`Array[State]`, `Array[Node2D]`) unless the user is explicitly prototyping, since untyped GDScript reads as either legacy (pre-4.0 habit) or a first draft rather than "how Godot wants it written."

---

## Part 3: Script-to-Node Wiring Idioms (`@onready`, `@export`, node paths)

Godot scripts aren't standalone classes — every script is normally attached to a node in a scene tree, and Godot has strong opinions about how that attachment should fetch its dependencies:

- `@onready var x = $Path/To/Node` — resolved once, right before `_ready()`, for caching a reference to a required child node. This is the standard way to avoid repeated `get_node()` calls.
- `@export var y: int = 10` — exposes a field to the Inspector so scene designers (or other collaborators) can configure instances without touching code — this is core to Godot's scene-composition philosophy, not just a convenience annotation.
- Unique node names (`%NodeName`) are the Godot 4 idiom for referencing a node anywhere in the local scene without a fragile relative path.

The architectural point underneath this: Godot wants configuration and wiring to live in the scene (`.tscn`) wherever possible, and scripts to read as "behavior," not "scene assembly." A script riddled with hardcoded `get_node("../../SomeNode")` calls is a code smell in Godot specifically, not just generically bad practice.

---

## Part 4: Signals Over Direct Coupling — The Big Architectural Preference

This is the part most LLM-generated GDScript gets wrong: it defaults to direct method calls and tight parent/child references (habits carried over from Unity/C# or generic OOP training data) instead of Godot's preferred event-driven decoupling.

Signals are Godot's version of the observer pattern — they let a node send out a message that other nodes can listen for and respond to, so instead of continuously polling a button to see if it's pressed, the button emits a signal when pressed. This decouples game objects: instead of forcing objects to expect other objects to always be present, they emit signals that any interested party can subscribe to.

The practical rule of thumb that shows up consistently in community best-practice writeups: connect signals via code (not just the editor UI) for anything non-trivial, use an autoload "Event Bus" for signals between nodes that are far apart in the scene tree, use shared state/resources for cross-cutting data, and actively guard against "signal spaghetti" once a project grows. The forum discourse around this ("When to use Signals vs Callable?") makes clear this isn't fully settled even among experienced users — so a prompt asking a model to generate Godot code should specify the decision rule explicitly rather than let the model guess:

- **Child → parent / outward communication**: always a signal. A child node should never assume a specific parent exists or call `get_parent().some_method()`.
- **Parent → child / downward, one-off command**: direct method call is fine (the parent legitimately owns the child).
- **Unrelated branches of the tree, or singletons↔scene**: signal through an Autoload/Event Bus, not a stored cross-reference.
- **UI ↔ game state**: signals both ways, usually mediated by a state resource or autoload, to keep UI code disposable/replaceable.

```gdscript
# health_component.gd — emits, doesn't know who's listening
class_name HealthComponent
extends Node

signal depleted
signal changed(current: int, max: int)

@export var max_health: int = 100
var current_health: int = max_health


func take_damage(amount: int) -> void:
    current_health = max(current_health - amount, 0)
    changed.emit(current_health, max_health)
    if current_health == 0:
        depleted.emit()
```

```gdscript
# player.gd — connects in code, reacts, no knowledge of who owns the health bar
extends CharacterBody2D

@onready var _health: HealthComponent = $HealthComponent


func _ready() -> void:
    _health.depleted.connect(_on_health_depleted)


func _on_health_depleted() -> void:
    queue_free()
```

---

## Part 5: Scenes vs. Scripts, Composition vs. Inheritance

Godot's official "Best Practices" documentation section (currently organized under headings like *Applying object-oriented principles in Godot*, *Scene organization*, *When to use scenes versus scripts*, and *Autoloads versus regular nodes*) is the canonical source for the architectural half of this question, as distinct from syntax. These pages cover applying object-oriented principles in Godot, scene organization, when to use scenes versus scripts, autoloads versus regular nodes, when and how to avoid using nodes for everything, Godot interfaces, and Godot notifications. The recurring theme across that section: prefer composing small, reusable scenes (like the `HealthComponent` above) over deep inheritance chains, reserve Autoloads for genuine global singletons (game state, event bus), and don't reach for a full `Node` subclass when a plain `RefCounted`/`Resource` class would do.

Implementation note if you're building this into a code-review or code-gen tool: treat "is this a Node-based scene component, or a plain data/logic class?" as the first branch, since it changes whether `@onready`, signals, and the scene tree apply at all.

---

## Standalone Copyable Prompt

```
You are generating or reviewing GDScript for Godot 4.x. Follow Godot's actual
conventions, not generic Python/OOP habits. Apply these rules in order:

STYLE (syntax-level, per the official GDScript style guide):
- snake_case for files, functions, variables, and signals; PascalCase for
  class/node names; CONSTANT_CASE for constants.
- Use full static typing on all variables, parameters, and return values
  (`var hp: int = 100`, `func heal(amount: int) -> void:`), including typed
  arrays (`Array[Node2D]`), unless explicitly told this is throwaway
  prototyping code.
- One statement per line. Blank line between function/class definitions.
  Double quotes by default; single quotes only to avoid escaping.
- Use `##` doc-comments above classes and exported members that need
  explanation, not `#`.
- Prefer the underscore-separated form for large numeric literals.

WIRING (how a script relates to its scene):
- Use `@onready var x = $Path` (or `%UniqueName` for anything not a direct,
  stable child) to cache node references, not repeated `get_node()` calls.
- Use `@export` for any value a scene designer or another dev should be able
  to configure from the Inspector instead of hardcoding it.
- Never write a script that reaches upward or sideways in the tree with a
  hardcoded relative path (e.g. `get_node("../../Foo")`). If it needs
  something outside its own subtree, that's a signal or Autoload's job, not
  a path.

ARCHITECTURE (how scripts should talk to each other):
- Child-to-parent or outward communication: always a signal, emitted with
  no knowledge of who (if anyone) is listening. Never call a method on
  `get_parent()`.
- Parent-to-child, one-off command where the parent legitimately owns the
  child: a direct method call is fine — don't over-engineer this into a
  signal.
- Communication between unrelated branches of the scene tree, or between a
  scene and global state: route it through an Autoload acting as an event
  bus or shared state holder, not a stored cross-reference between nodes
  that don't own each other.
- Default to composing small, single-purpose scenes/components (e.g. a
  `HealthComponent`, a `HitboxComponent`) over deep class inheritance chains.
- Before writing a `Node`-based script, ask whether this really needs to be
  part of the scene tree, or whether a plain `RefCounted`/`Resource` class
  is sufficient and cheaper.

When reviewing existing code instead of generating new code, flag violations
of the above under three separate headings — Style, Wiring, Architecture —
rather than a single flat list, and explain the "why" (usually decoupling,
editor tooling support, or performance) for anything non-cosmetic you flag.

Task: [INSERT SPECIFIC SCRIPT, FEATURE, OR CODE-REVIEW TARGET HERE]
```

---

## Reference Lineage / Further Reading

- Godot Docs — [GDScript style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html) (canonical syntax/formatting rules)
- Godot Docs — [Best Practices index](https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html) (scene organization, OOP-in-Godot, scenes vs. scripts, autoloads)
- Godot Docs — [Signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html) (observer pattern, connecting signals)
- febucci.com — [Godot Signals Architecture: Best Practices & Event Bus](https://blog.febucci.com/2024/12/godot-signals-architecture/) (practical connect-in-code / event-bus / avoid-signal-spaghetti guidance)
- Godot Forum — [When to use Signals vs Callable?](https://forum.godotengine.org/t/when-to-use-signals-vs-callable-best-practices/100097) (shows this is genuinely debated, not fully settled, even among experienced users)
- GDQuest/community — [GDScript-formatter](https://github.com/DevTwilight/GDScript-formatter) (automatable ground-truth for style-guide conformance)
