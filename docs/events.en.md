```markdown
# Events

The engine emits events that you can hook into to update your UI.

## Listening to Events

```python
game.events.on("night_started", lambda round_num, actors: print(f"Night {round_num}"))
```

## Event Reference

| Event | Arguments | Description |
|-------|-----------|-------------|
| `game_started` | `players` (list of Player) | Game has started, roles assigned. |
| `night_started` | `round_number`, `actors` (list of Player) | Night phase begins. `actors` are those who can act. |
| `night_action` | `actor_id`, `target_id` | One night action was recorded. |
| `day_started` | `round_number` | Day phase begins. |
| `vote_cast` | `voter_id`, `target_id` | A vote was recorded. |
| `player_killed` | `player` (Player), `cause` (str) | A player died. |
| `game_over` | `winner` (str) | Game ended. Winner can be "village", "werewolf", or a custom team name. |
```