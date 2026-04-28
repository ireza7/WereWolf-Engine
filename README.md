# WereWolf-Engine
---

## `README.md` – محتوای پیشنهادی

(فایل `README.md` را در ریشهٔ پروژه بساز و متن زیر را جایگذاری کن. بخش `نام تو` و لینک‌ها را شخصی‌سازی کن.)

```markdown
# WereWolf Engine

A flexible, extensible Werewolf (Mafia) game engine for Python.  
Build your own bot, web app, or CLI game using a clean library with no I/O dependencies.

## Features

- 🎭 **6 built‑in roles:** Villager, Werewolf, Seer, Doctor, Witch, Hunter.
- 🔌 **Plugin‑friendly role system:** Register custom roles without touching the engine code.
- 🌙 **Full night/day cycle** with priority‑based night actions and conflict resolution.
- 🗳️ **Voting system** with majority rule and tie handling.
- 📡 **Event bus:** Hook into game events (`night_started`, `player_killed`, `game_over`, …) to drive your UI.
- 📦 **Serialization:** Save complete game state with `to_dict()` and restore with `from_dict()` – perfect for databases.
- ✅ **Thoroughly tested:** 23+ automated tests covering all roles and phases.

## Installation

```bash
pip install werewolf-engine
```

*Note: The package is published on PyPI (coming soon). For the development version:*

```bash
git clone https://github.com/your-username/WereWolf-Engine.git
cd WereWolf-Engine
pip install -e ".[dev]"
```

## Quick Start

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={
    "villager": 3,
    "seer": 1,
    "doctor": 1,
    "werewolf": 2,
    "witch": 1,
    "hunter": 1,
})

game = Game(["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy"], config)

# Register event listeners (optional)
game.events.on("game_started", lambda players: print("Game started!"))
game.events.on("night_started", lambda r, actors: print(f"Night {r}, actors: {[p.name for p in actors]}"))
game.events.on("player_killed", lambda player, cause: print(f"{player.name} died by {cause}"))
game.events.on("game_over", lambda winner: print(f"Winner: {winner}"))

game.start()

# Example: executing all night actions automatically (adapt for your UI)
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        nm = game.night_manager
        actor = nm.current_actor
        if actor:
            targets = nm.get_available_targets(actor)
            if targets:
                game.night_action(actor.id, targets[0].id)
            else:
                game.night_skip(actor.id)
    elif game.phase == Phase.DAY:
        dm = game.day_manager
        # ... get votes from users ...
```

## Built‑in Roles

| Role | Team | Night Action | Special Ability |
|------|------|--------------|-----------------|
| **Villager** | Village | None | – |
| **Werewolf** | Werewolf | Kill one non‑werewolf | Knows pack mates |
| **Seer** | Village | Investigate one player | Learns if target is werewolf or not |
| **Doctor** | Village | Protect one player | Cannot protect the same target two nights in a row |
| **Witch** | Village | Use two potions (heal & kill) once per game | Heal can be used on the night’s victim; kill can target any alive player |
| **Hunter** | Village | None | When killed (by any cause), shoots one alive player |

## Adding Custom Roles

1. Subclass `werewolf_engine.roles.base.BaseRole`.
2. Override necessary methods (`can_act_night`, `perform_night_action`, `get_available_targets`, …).
3. Register it:

```python
from werewolf_engine.roles import register_role

class Cupid(BaseRole):
    name = "cupid"
    team = "village"
    night_priority = 5
    # ... methods ...

register_role("cupid", Cupid)
```

Now you can use `"cupid"` in your `GameConfig.role_counts`.

For a distributable plugin, use Python entry points (see [Advanced Usage](#)).

## Game Events

Attach callbacks to the `Game.events` bus:

```python
game.events.on("night_started", lambda round_num, actors: broadcast(...))
```

Available events:
- `game_started` (players)
- `night_started` (round_number, actors)
- `night_action` (actor_id, target_id)
- `day_started` (round_number)
- `vote_cast` (voter_id, target_id)
- `player_killed` (player, cause)
- `game_over` (winner)

## State & Serialization

Get public/private state for all players:

```python
# Public view (everyone)
public = game.get_public_state()
# {"phase": "day", "round": 2, "players": [...], ...}

# Private view for a specific player (role, team, private info)
private = game.get_private_state(player_id)
# {"my_role": "seer", "my_team": "village", "private_info": {...}, ...}
```

Save and restore a game:

```python
data = game.to_dict()
# store in database / Redis ...

restored_game = Game.from_dict(data)
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a branch for your feature or fix.
3. Add tests.
4. Submit a pull request.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.
```

---

## گام بعدی

پس از نوشتن `README.md`، آن را commit و push کن:

```powershell
git add README.md
git commit -m "Add comprehensive README"
git push
```