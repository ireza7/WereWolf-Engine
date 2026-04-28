from __future__ import annotations
from typing import List, TYPE_CHECKING

from .base import BaseRole
from ..player import Player

if TYPE_CHECKING:
    from ..game import Game


class Seer(BaseRole):
    name = "seer"
    team = "village"
    night_priority = 10

    # ----- وضعیت داخلی -----
    def __init__(self):
        self._last_result: dict | None = None   # نتیجهٔ دیشب

    # ----- هوک‌های شب -----
    def can_act_night(self, game: "Game", player: "Player") -> bool:
        return True   # هر شب می‌تواند

    def get_available_targets(self, game: "Game", player: "Player") -> List["Player"]:
        # همهٔ بازیکنان زنده (حتی خودش)
        return [p for p in game.players if p.is_alive()]

    def perform_night_action(self, game: "Game", actor: "Player", target: "Player") -> None:
        # استعلام: آیا هدف گرگینه است؟
        is_wolf = target.role.team == "werewolf"
        self._last_result = {
            "target_id": target.id,
            "target_name": target.name,
            "result": "werewolf" if is_wolf else "not werewolf",
        }

    # ----- اطلاعات خصوصی -----
    def get_private_info(self, game: "Game", player: "Player") -> dict:
        info = super().get_private_info(game, player)
        if self._last_result:
            info["seer_last_result"] = self._last_result
        return info