from __future__ import annotations
from abc import ABC
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game
    from ..player import Player


class BaseRole(ABC):
    """کلاس پایه برای تمام نقش‌های بازی Werewolf."""

    # این ویژگی‌ها باید در هر زیرکلاس بازنویسی شوند
    name: str = "base"
    team: str = "village"       # "village", "werewolf", "solo"
    night_priority: int = 0     # عدد کمتر یعنی زودتر عمل می‌کند

    # ------------------------------------------------------------------
    # متدهایی که هر نقش می‌تواند بازنویسی کند
    # ------------------------------------------------------------------

    def can_act_night(self, game: "Game", player: "Player") -> bool:
        """آیا این بازیکن در شب جاری می‌تواند عملی انجام دهد؟"""
        return False

    def get_available_targets(self, game: "Game", player: "Player") -> List["Player"]:
        """لیست بازیکنانی که می‌توانند هدف این نقش قرار بگیرند."""
        return []

    def perform_night_action(self, game: "Game", actor: "Player", target: "Player") -> None:
        """عملیات شبانه را اجرا کن و وضعیت بازی را تغییر بده."""
        pass

    def get_private_info(self, game: "Game", player: "Player") -> dict:
        """
        اطلاعات خصوصی‌ای که فقط صاحب این نقش باید ببیند.
        مثال برای پیشگو: {"seer_result": "werewolf"}
        """
        return {}

    def on_player_died(self, game: "Game", dead_player: "Player", cause: str) -> None:
        """
        هوکی که وقتی هر بازیکنی می‌میرد صدا زده می‌شود.
        برای نقش‌هایی مثل شکارچی یا جادوگر که باید واکنش نشان دهند.
        """
        pass

    def on_vote_result(self, game: "Game", eliminated: "Player") -> None:
        """
        هوکی که بعد از رأی‌گیری روز صدا زده می‌شود.
        """
        pass