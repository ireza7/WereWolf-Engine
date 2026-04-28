```markdown
# API Reference

This section covers the main classes and functions exposed by the werewolf engine.

## Game

The central class that manages the entire game flow.

### `Game(player_names, config=None)`
Creates a new game instance.

- `player_names` (list of str): Names of the players.
- `config` (GameConfig, optional): Game configuration. If not provided, uses an empty config (roles must be assigned manually).

### Properties
- `players` (list of Player): All players.
- `phase` (Phase): Current game phase.
- `round_number` (int): Current round (starts at 1 after `start()`).
- `events` (GameEvents): The event bus.
- `night_manager` (NightManager or None): Active night manager (only during NIGHT phase).
- `day_manager` (DayManager or None): Active day manager (only during DAY phase).

### Methods
- `start()`: Assigns roles (via config) and starts the first night.
- `night_action(actor_id, target_id)`: Submits a night action for the current actor.
- `night_skip(actor_id)`: Skips the current actor's turn (when no valid target).
- `day_vote(voter_id, target_id)`: Casts a day vote.
- `get_public_state()`: Returns a dict with public game state.
- `get_private_state(player_id)`: Returns a dict with private info for a player.
- `to_dict()`: Serializes complete game state to a dict.
- `from_dict(data)`: Classmethod to restore a game from a dict.

## Player

Represents a player.

### `Player(player_id, name)`
- `id` (int): Unique identifier.
- `name` (str): Display name.
- `alive` (bool): Whether the player is alive.
- `assign_role(role)`: Assigns a role instance to the player.
- `kill()`: Sets `alive` to False.

## GameConfig

Configuration dataclass.

### `GameConfig(role_counts=None, max_players=20, reveal_role_on_death=False)`
- `role_counts` (dict[str, int]): Mapping from role name to count.
- `max_players` (int): Maximum allowed players.
- `reveal_role_on_death` (bool): If True, dead player's role is made public.

## Phase

Enum with values: `LOBBY`, `NIGHT`, `DAY`, `END`.

## GameEvents

Simple event bus.

- `on(event_name, callback)`: Register a callback.
- `emit(event_name, *args, **kwargs)`: Call all handlers for an event.

## Roles

### BaseRole

Abstract base class for all roles. Defines the following interface (all optional to override):

- `name` (str): Role identifier.
- `team` (str): "village", "werewolf", or a custom team.
- `night_priority` (int): Lower values act first (e.g., Seer 10, Werewolf 30).
- `can_act_night(game, player) -> bool`: Whether the player can act this night.
- `get_available_targets(game, player) -> list[Player]`: Valid target list for the UI.
- `perform_night_action(game, actor, target)`: Execute the night action.
- `get_private_info(game, player) -> dict`: Private data shown only to that player.
- `on_player_died(game, dead_player, cause)`: Hook called when any player dies.
- `on_vote_result(game, eliminated)`: Hook called after daily vote.

### Registry

- `register_role(name: str, role_cls: Type[BaseRole])`: Registers a role class.
- `get_role_class(name: str) -> Type[BaseRole]`: Returns the class for a role name.
- `get_all_role_names() -> list[str]`: Lists all registered roles.

## Error Types

- `WerewolfEngineError`: Base exception.
- `InvalidActionError`: Raised when an action is invalid.
- `NotYourTurnError`: Raised when it's not the player's turn.
- `GameNotStartedError`: Raised when an operation is called before game start.
- `GameOverError`: Raised when an operation is called after game over.
- `PlayerNotFoundError`: Raised for an invalid player ID.
```