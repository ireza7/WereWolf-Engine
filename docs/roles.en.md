```markdown
# Roles

The engine ships with six roles. You can easily add your own.

| Role | Team | Night Action | Special |
|------|------|--------------|---------|
| Villager | Village | None | – |
| Werewolf | Werewolf | Kill one non‑werewolf | Knows pack mates |
| Seer | Village | Investigate one player | Learns `werewolf` or `not werewolf` |
| Doctor | Village | Protect one player | Cannot protect the same player twice in a row |
| Witch | Village | Use two potions (heal / kill) once per game | Heal can save the night’s victim; kill can target any alive player |
| Hunter | Village | None | When killed (by any cause), shoots one alive player |

## Creating a Custom Role

1. Subclass `werewolf_engine.roles.base.BaseRole`.
2. Override the methods you need (e.g., `can_act_night`, `perform_night_action`).
3. Register it:

```python
from werewolf_engine.roles import register_role, BaseRole

class Cupid(BaseRole):
    name = "cupid"
    team = "village"
    night_priority = 5

    def can_act_night(self, game, player):
        return True  # only once? you decide

    def get_available_targets(self, game, player):
        return [p for p in game.players if p.is_alive()]

    def perform_night_action(self, game, actor, target):
        # your logic
        pass

register_role("cupid", Cupid)
```

Now `"cupid"` can be used in `GameConfig.role_counts`.

See [API Reference](api-reference.md) for the complete `BaseRole` interface.
```