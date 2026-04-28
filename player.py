from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .roles.base import BaseRole


class Player:
    """یک بازیکن در بازی."""

    def __init__(self, player_id: int, name: str):
        self.id: int = player_id
        self.name: str = name
        self.alive: bool = True
        self._role: Optional["BaseRole"] = None
        self._protected: bool = False

    @property
    def role(self) -> Optional["BaseRole"]:
        return self._role

    def assign_role(self, role: "BaseRole") -> None:
        """نقش بازیکن را تنظیم کن. فقط یک بار صدا زده می‌شود."""
        if self._role is not None:
            raise RuntimeError("نقش این بازیکن از قبل تنظیم شده است.")
        self._role = role

    def kill(self) -> None:
        """بازیکن را بکش."""
        self.alive = False

    def is_alive(self) -> bool:
        return self.alive

    def __repr__(self):
        return f"Player(id={self.id}, name='{self.name}', alive={self.alive}, role={self.role.name if self.role else 'None'})"