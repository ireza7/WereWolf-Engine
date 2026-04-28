import random
from typing import List, TYPE_CHECKING

from ..roles import get_role_class

if TYPE_CHECKING:
    from ..game import Game
    from ..config import GameConfig

def assign_roles(game: "Game", config: "GameConfig") -> None:
    """
    بر اساس تنظیمات، به بازیکنان نقش تصادفی بدهد.
    تعداد نقش‌ها باید با تعداد بازیکنان برابر باشد.
    """
    role_names = []
    for role_name, count in config.role_counts.items():
        role_names.extend([role_name] * count)

    if len(role_names) != len(game.players):
        raise ValueError(
            f"تعداد نقش‌ها ({len(role_names)}) با تعداد بازیکنان ({len(game.players)}) برابر نیست."
        )

    random.shuffle(role_names)
    for player, role_name in zip(game.players, role_names):
        role_class = get_role_class(role_name)
        role_instance = role_class()   # هر نقش یک نمونه جدید
        player.assign_role(role_instance)