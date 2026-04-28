from __future__ import annotations
from typing import List, TYPE_CHECKING

from .base import BaseRole
from ..player import Player

if TYPE_CHECKING:
    from ..game import Game


class Werewolf(BaseRole):
    name = "werewolf"
    team = "werewolf"
    night_priority = 30

    # ----- هوک‌های شب -----
    def can_act_night(self, game: "Game", player: "Player") -> bool:
        return True

    def get_available_targets(self, game: "Game", player: "Player") -> List["Player"]:
        # هر بازیکن زنده‌ای که گرگینه نباشد
        return [
            p for p in game.players
            if p.is_alive() and p.role.team != "werewolf"
        ]

    def perform_night_action(self, game: "Game", actor: "Player", target: "Player") -> None:
        # ثبت هدف شکار امشب (توسط هر گرگینه)
        game._wolf_target_id = target.id

    # ----- اطلاعات خصوصی -----
    def get_private_info(self, game: "Game", player: "Player") -> dict:
        info = super().get_private_info(game, player)
        # هم‌تیمی‌ها را نشان بده
        pack = [
            {"id": p.id, "name": p.name}
            for p in game.players
            if p.is_alive() and p.role.team == "werewolf" and p.id != player.id
        ]
        if pack:
            info["fellow_wolves"] = pack
        return info