from dataclasses import dataclass, field
from typing import Dict


@dataclass
class GameConfig:
    """
    پیکربندی یک دست بازی.

    Attributes:
        role_counts: دیکشنری از نام نقش به تعداد آن در بازی.
                     اگر خالی باشد، می‌تواند بعداً در Lobby پر شود.
        max_players: حداکثر تعداد بازیکنان (برای اعتبارسنجی).
        reveal_role_on_death: آیا نقش بازیکن حذف‌شده به همه نشان داده شود؟
    """
    role_counts: Dict[str, int] = field(default_factory=dict)
    max_players: int = 20
    reveal_role_on_death: bool = False