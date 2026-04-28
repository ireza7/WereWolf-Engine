from __future__ import annotations
from typing import TYPE_CHECKING
import random

from .base import BaseRole
from ..player import Player

if TYPE_CHECKING:
    from ..game import Game


class Hunter(BaseRole):
    name = "hunter"
    team = "village"
    night_priority = 0   # عمل شبانه ندارد

    # ----- هوک مرگ -----
    def on_player_died(self, game: "Game", dead_player: "Player", cause: str) -> None:
        # فقط وقتی خود شکارچی بمیرد (به هر علتی غیر از "protected")
        if dead_player.role != self:
            return
        if cause == "protected":
            return

        # انتخاب یک قربانی تصادفی از بین زنده‌ها (غیر از خودش)
        alive = [p for p in game.players if p.is_alive() and p.id != dead_player.id]
        if alive:
            victim = random.choice(alive)
            victim.kill()
            # رویداد مرگ قربانی
            game.events.emit("player_killed", victim, cause="hunter_revenge")

    # ----- اطلاعات خصوصی -----
    def get_private_info(self, game: "Game", player: "Player") -> dict:
        return {}