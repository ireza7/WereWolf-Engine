# werewolf_engine/phases/night.py
from ..roles.base import BaseRole
from ..player import Player
from ..errors import InvalidActionError, NotYourTurnError
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game


class NightManager:
    def __init__(self, game: "Game"):
        self.game = game
        ordered = []
        for p in game.players:
            if p.is_alive() and p.role and p.role.can_act_night(game, p):
                ordered.append(p)
        ordered.sort(key=lambda p: p.role.night_priority)
        self._actors = ordered
        self._current_index = 0
        game._wolf_target_id = None
        for p in game.players:
            p._protected = False
        game._night_kill_victims = []

    @property
    def current_actor(self) -> Optional[Player]:
        if self._current_index < len(self._actors):
            return self._actors[self._current_index]
        return None

    def get_available_targets(self, player: Player) -> List[Player]:
        return player.role.get_available_targets(self.game, player)

    def submit_action(self, actor_id: int, target_id: int) -> None:
        current = self.current_actor
        if current is None:
            raise NotYourTurnError("همه بازیکنان شب عمل کرده‌اند.")
        if current.id != actor_id:
            raise NotYourTurnError(f"نوبت بازیکن {current.name} است، نه شما.")
        target = self.game._get_player(target_id)
        available = self.get_available_targets(current)
        if target not in available:
            raise InvalidActionError("هدف نامعتبر است.")
        current.role.perform_night_action(self.game, current, target)
        self._current_index += 1

    def skip_action(self, actor_id: int) -> None:
        current = self.current_actor
        if current is None:
            raise NotYourTurnError("همه بازیکنان شب عمل کرده‌اند.")
        if current.id != actor_id:
            raise NotYourTurnError(f"نوبت بازیکن {current.name} است، نه شما.")
        self._current_index += 1

    def all_actions_submitted(self) -> bool:
        return self._current_index >= len(self._actors)

    def resolve(self) -> None:
        kills: List[tuple] = []

        wolf_target_id = self.game._wolf_target_id
        if wolf_target_id is not None:
            wolf_target = self.game._get_player(wolf_target_id)
            if wolf_target.is_alive():
                kills.append((wolf_target, "werewolf"))

        for p in self.game.players:
            if p.is_alive() and isinstance(p.role, BaseRole) and p.role.name == "witch":
                witch = p.role
                kill_id = getattr(witch, '_kill_target_id', None)
                if kill_id is not None:
                    target = self.game._get_player(kill_id)
                    if target.is_alive():
                        kills.append((target, "witch"))

        saved: set = set()
        for p in self.game.players:
            if p._protected:
                saved.add(p.id)
        for p in self.game.players:
            if p.is_alive() and isinstance(p.role, BaseRole) and p.role.name == "witch":
                heal_id = getattr(p.role, '_heal_target_id', None)
                if heal_id is not None:
                    saved.add(heal_id)

        final_kills = [(target, cause) for target, cause in kills if target.id not in saved]

        for target, cause in final_kills:
            target.kill()
            self.game.events.emit("player_killed", target, cause=cause)
            if target.role:
                target.role.on_player_died(self.game, target, cause=cause)

        for p in self.game.players:
            if p.role and hasattr(p.role, '_on_night_ended'):
                p.role._on_night_ended()
        self.game._wolf_target_id = None