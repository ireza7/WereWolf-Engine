from __future__ import annotations
from typing import List, TYPE_CHECKING

from .base import BaseRole
from ..player import Player

if TYPE_CHECKING:
    from ..game import Game


class Witch(BaseRole):
    name = "witch"
    team = "village"
    night_priority = 40

    def __init__(self):
        self._heal_used = False
        self._kill_used = False
        # اهداف امشب (پرچم موقت، قبل از حل تعارض)
        self._heal_target_id: int | None = None
        self._kill_target_id: int | None = None

    # ----- هوک‌های شب -----
    def can_act_night(self, game: "Game", player: "Player") -> bool:
        # اگر حداقل یک معجون داشته باشد
        return not self._heal_used or not self._kill_used

    def get_available_targets(self, game: "Game", player: "Player") -> List["Player"]:
        candidates = []
        if not self._heal_used:
            victims = getattr(game, "_night_kill_victims", [])
            for v in victims:
                candidates.append(v)
        if not self._kill_used:
            for p in game.players:
                if p.is_alive() and p not in candidates:
                    candidates.append(p)
        return candidates

    def perform_night_action(self, game: "Game", actor: "Player", target: "Player") -> None:
        # تشخیص: آیا این هدف برای نجات است یا کشتن؟
        # ساده‌ترین راه: اگر target جزو victims شب است، نجات بده.
        victims = getattr(game, "_night_kill_victims", [])
        if target in victims and not self._heal_used:
            self._heal_target_id = target.id
            self._heal_used = True
        elif not self._kill_used:
            self._kill_target_id = target.id
            self._kill_used = True

    # ----- هوک پایان شب -----
    def _on_night_ended(self):
        self._heal_target_id = None
        self._kill_target_id = None

    # ----- اطلاعات خصوصی -----
    def get_private_info(self, game: "Game", player: "Player") -> dict:
        info = super().get_private_info(game, player)
        info["heal_available"] = not self._heal_used
        info["kill_available"] = not self._kill_used
        return info