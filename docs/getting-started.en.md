# Getting Started

## Installation

```bash
pip install werewolf-engine
```

For the latest development version:

```bash
git clone https://github.com/your-username/WereWolf-Engine
cd WereWolf-Engine
pip install -e ".[dev]"
```

## Basic Usage

### 1. Create a Game

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={
    "villager": 3,
    "werewolf": 2,
    "seer": 1,
    "doctor": 1,
    "witch": 1,
    "hunter": 1
})

game = Game(["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy"], config)
```

### 2. Listen to Events (Optional)

```python
game.events.on("game_started", lambda players: print("Game started!"))
game.events.on("night_started", lambda round_num, actors: print(f"Night {round_num}"))
game.events.on("player_killed", lambda player, cause: print(f"{player.name} died by {cause}"))
game.events.on("game_over", lambda winner: print(f"Winner: {winner}"))
```

### 3. Start the Game

```python
game.start()
```

Now the game is in the **Night** phase. You must iterate over the actors provided by `game.night_manager` and collect their choices.

### 4. Driving a Night Phase

```python
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        nm = game.night_manager
        while not nm.all_actions_submitted():
            actor = nm.current_actor
            if actor:
                targets = nm.get_available_targets(actor)
                # Ask the user (or AI) to choose a target
                chosen = get_user_choice(actor, targets)
                if chosen is not None:
                    game.night_action(actor.id, chosen.id)
                else:
                    game.night_skip(actor.id)   # when no valid target
        # Night ends automatically after the last action
```

### 5. Driving a Day Phase

```python
    elif game.phase == Phase.DAY:
        dm = game.day_manager
        while not dm.all_votes_submitted():
            voter = dm.current_voter   # however your UI works
            # get vote from user
            target = get_vote(voter)
            game.day_vote(voter.id, target.id)
        # Day ends after all votes are cast
```

### 6. Accessing Game State

Public state for everyone:

```python
public = game.get_public_state()
# {"phase": "day", "round": 2, "players": [...], ...}
```

Private state for a specific player:

```python
private = game.get_private_state(player_id)
# {"my_role": "seer", "my_team": "village", "private_info": {...}}
```

### 7. Saving and Restoring

```python
data = game.to_dict()
# store in database / Redis ...

restored_game = Game.from_dict(data)
```

## Next Steps

- Learn about the built‑in [Roles](roles.md).
- Use the [Event system](events.md) to build a real‑time bot.
- Check the [API Reference](api-reference.md) for internal details.
```