from __future__ import annotations
from typing import List, TYPE_CHECKING

from .base import BaseRole
from ..player import Player

if TYPE_CHECKING:
    from ..game import Game


class Doctor(BaseRole):
    name = "doctor"
    team = "village"
    night_priority = 20

    def __init__(self):
        self._last_protected_id: int | None = None   # نفر دیشب
        self._protected_tonight_id: int | None = None  # نفر امشب (برای استفاده در حل تعارض)

    # ----- هوک‌های شب -----
    def can_act_night(self, game: "Game", player: "Player") -> bool:
        return True

    def get_available_targets(self, game: "Game", player: "Player") -> List["Player"]:
        candidates = [p for p in game.players if p.is_alive()]
        # حذف کسی که دیشب محافظت شده (اگر بازی بیش از یک شب گذشته باشد)
        if self._last_protected_id is not None:
            candidates = [p for p in candidates if p.id != self._last_protected_id]
        return candidates

    def perform_night_action(self, game: "Game", actor: "Player", target: "Player") -> None:
        # ثبت محافظت امشب
        self._protected_tonight_id = target.id
        # نشانه‌گذاری روی بازیکن (بعداً در حل تعارض شب استفاده می‌شود)
        target._protected = True

    # ----- هوک پایان شب (برای به‌روزرسانی داخلی) -----
    def _on_night_ended(self):
        """بعد از حل تعارض شب صدا زده می‌شود."""
        self._last_protected_id = self._protected_tonight_id
        self._protected_tonight_id = None

    # ----- اطلاعات خصوصی -----
    def get_private_info(self, game: "Game", player: "Player") -> dict:
        info = super().get_private_info(game, player)
        if self._protected_tonight_id is not None:
            info["protected_tonight"] = self._protected_tonight_id
        if self._last_protected_id is not None:
            info["cannot_protect"] = self._last_protected_id
        return info