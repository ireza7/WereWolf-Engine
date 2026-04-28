# werewolf_engine/roles/hunter.py
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
    night_priority = 0

    def __init__(self):
        self._revenge_used = False

    def on_player_died(self, game: "Game", dead_player: "Player", cause: str) -> None:
        if dead_player.role is not self:
            return
        if cause == "protected":
            return
        if self._revenge_used:
            return

        alive = [p for p in game.players if p.is_alive() and p.id != dead_player.id]
        if alive:
            victim = random.choice(alive)
            victim.kill()
            self._revenge_used = True
            game.events.emit("player_killed", victim, cause="hunter_revenge")

    def get_private_info(self, game: "Game", player: "Player") -> dict:
        return {}