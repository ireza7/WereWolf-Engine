# WereWolf Engine

A flexible, extensible Werewolf (Mafia) game engine for Python.

[مستندات فارسی](https://github.com/ireza7/WereWolf-Engine/wiki/Home-fa) | [README فارسی](README-fa.md)

[![Tests](https://github.com/ireza7/WereWolf-Engine/actions/workflows/tests.yml/badge.svg)](https://github.com/ireza7/WereWolf-Engine/actions)
[![PyPI version](https://badge.fury.io/py/werewolf-engine.svg)](https://pypi.org/project/werewolf-engine/)

## Features

- 6 built‑in roles: Villager, Werewolf, Seer, Doctor, Witch, Hunter
- Plugin system for custom roles
- Full night/day cycle with priority and conflict resolution
- Voting system with majority & tie handling
- Event bus for UI integration
- Save/restore game state (to/from dict)
- 23+ tests covering all features

## Installation

```bash
pip install werewolf-engine
```

## Quick Example

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={"villager": 3, "werewolf": 2, "seer": 1, "doctor": 1, "witch": 1, "hunter": 1})
game = Game(["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy"], config)
game.start()

# Drive the game with your own UI
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        actor = game.night_manager.current_actor
        if actor:
            targets = game.night_manager.get_available_targets(actor)
            game.night_action(actor.id, chosen_target.id)
```

## Documentation

Full documentation is available in **English** and **Persian** on the [GitHub Wiki](https://github.com/ireza7/WereWolf-Engine/wiki).

- [Home](https://github.com/ireza7/WereWolf-Engine/wiki/Home)
- [Getting Started](https://github.com/ireza7/WereWolf-Engine/wiki/Getting-Started)
- [Roles](https://github.com/ireza7/WereWolf-Engine/wiki/Roles)
- [Events](https://github.com/ireza7/WereWolf-Engine/wiki/Events)
- [API Reference](https://github.com/ireza7/WereWolf-Engine/wiki/API-Reference)
- [Contributing](https://github.com/ireza7/WereWolf-Engine/wiki/Contributing)

## License

This project is licensed under the MIT License.
