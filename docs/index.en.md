```markdown
# WereWolf Engine

**A flexible, extensible Werewolf (Mafia) game engine for Python.**

Build your own Telegram bot, web app, or CLI game with a clean library that has zero I/O dependencies.

## Features

- 🎭 **6 built‑in roles:** Villager, Werewolf, Seer, Doctor, Witch, Hunter.
- 🔌 **Plugin‑friendly role system:** Register custom roles without touching the engine code.
- 🌙 **Full night/day cycle** with priority‑based night actions and conflict resolution.
- 🗳️ **Voting system** with majority rule and tie handling.
- 📡 **Event bus:** Hook into game events to drive your UI.
- 💾 **Serialization:** Save and restore complete game state with `to_dict()` / `from_dict()`.
- ✅ **Thoroughly tested:** 23+ automated tests covering all roles and phases.

## Quick Example

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={
    "villager": 3,
    "werewolf": 2,
    "seer": 1,
    "doctor": 1,
    "witch": 1,
    "hunter": 1,
})

game = Game(["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy"], config)
game.start()

# Drive the game with your own UI
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        actor = game.night_manager.current_actor
        if actor:
            targets = game.night_manager.get_available_targets(actor)
            # get user input, then:
            game.night_action(actor.id, choice)
    # ... handle day voting similarly
```

Head over to the [Getting Started](getting-started.md) guide for detailed instructions.
```