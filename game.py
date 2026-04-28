from __future__ import annotations
from typing import List, Optional, Dict, Any

from .player import Player
from .events import GameEvents
from .config import GameConfig
from .errors import (
    GameNotStartedError,
    GameOverError,
    PlayerNotFoundError,
)
from .phases import Phase
from .phases.lobby import assign_roles
from .phases.night import NightManager
from .phases.day import DayManager

class Game:
    """موتور اصلی یک دست بازی Werewolf.

    مصرف‌کننده (ربات) به ترتیب زیر عمل می‌کند:
    ۱. نمونه‌سازی با نام بازیکنان و تنظیمات
    ۲. `game.start()` → آغاز بازی
    ۳. در فاز شب: برای هر `actor` که `night_manager` معرفی می‌کند،
       اهداف مجاز را بخوانید و از کاربر انتخاب بگیرید،
       سپس `game.night_action(actor_id, target_id)` صدا بزنید.
       وقتی همه عمل کردند، شب خودکار به روز می‌رود.
    ۴. در فاز روز: مشابه مرحله ۳ برای رأی‌گیری.
    """

    def __init__(self, player_names: List[str], config: Optional[GameConfig] = None):
        if config is None:
            config = GameConfig()
        self.config = config
        self.events = GameEvents()
        self.players = [
            Player(i, name) for i, name in enumerate(player_names)
        ]
        self.phase = Phase.LOBBY
        self.round_number = 0

        # برای هماهنگی شب
        self._wolf_target_id: Optional[int] = None

        # مدیریت‌کنندهٔ شب و روز (زمانی که در آن فاز باشیم)
        self.night_manager: Optional[NightManager] = None
        self.day_manager: Optional[DayManager] = None

    # ------------------------------------------------------------------
    # شروع بازی
    # ------------------------------------------------------------------
    def start(self) -> None:
        """نقش‌ها را انتساب می‌دهد و وارد فاز شب اول می‌شود."""
        if self.phase != Phase.LOBBY:
            raise GameNotStartedError("بازی قبلاً شروع شده یا به اتمام رسیده است.")

        assign_roles(self, self.config)
        self.round_number = 1
        self.events.emit("game_started", self.players)
        self._start_night()

    # ------------------------------------------------------------------
    # گردش فاز شب
    # ------------------------------------------------------------------
    def _start_night(self) -> None:
        self.phase = Phase.NIGHT
        self.night_manager = NightManager(self)
        self.events.emit("night_started", self.round_number, self.night_manager._actors)

    def night_action(self, actor_id: int, target_id: int) -> None:
        """ثبت عملیات یک بازیکن در شب جاری."""
        if self.phase != Phase.NIGHT:
            raise GameNotStartedError("اکنون فاز شب نیست.")
        if self.night_manager is None:
            raise RuntimeError("مدیر شب مقداردهی نشده است.")

        self.night_manager.submit_action(actor_id, target_id)
        self.events.emit("night_action", actor_id, target_id)

        if self.night_manager.all_actions_submitted():
            self._end_night()

    def _end_night(self) -> None:
        """پایان شب: حل تعارض، اعمال مرگ، رفتن به روز."""
        self.night_manager.resolve()
        self.night_manager = None

        if self._check_game_over():
            return

        self._start_day()

    # ------------------------------------------------------------------
    # گردش فاز روز
    # ------------------------------------------------------------------
    def _start_day(self) -> None:
        self.phase = Phase.DAY
        self.day_manager = DayManager(self)
        self.events.emit("day_started", self.round_number)

    def day_vote(self, voter_id: int, target_id: int) -> None:
        """ثبت رأی یک بازیکن در روز جاری."""
        if self.phase != Phase.DAY:
            raise GameNotStartedError("اکنون فاز روز نیست.")
        if self.day_manager is None:
            raise RuntimeError("مدیر روز مقداردهی نشده است.")

        self.day_manager.cast_vote(voter_id, target_id)
        self.events.emit("vote_cast", voter_id, target_id)

        if self.day_manager.all_votes_submitted():
            self._end_day()

    def _end_day(self) -> None:
        """پایان روز: تعیین رأی‌گیری، اعمال حذف، رفتن به شب بعدی."""
        eliminated = self.day_manager.resolve()
        self.day_manager = None

        if eliminated:
            # بررسی نقش‌های واکنشی (مثل شکارچی) قبلاً در on_player_died اعمال شده.
            pass

        if self._check_game_over():
            return

        # رفتن به شب بعدی
        self.round_number += 1
        self._start_night()

    # ------------------------------------------------------------------
    # شرایط پایان بازی
    # ------------------------------------------------------------------
    def _check_game_over(self) -> bool:
        alive = [p for p in self.players if p.is_alive()]
        werewolves = [p for p in alive if p.role and p.role.team == "werewolf"]
        villagers = [p for p in alive if p.role and p.role.team != "werewolf"]

        if not werewolves:
            self._end_game("village")
            return True
        if len(werewolves) >= len(villagers):
            self._end_game("werewolf")
            return True
        return False

    def _end_game(self, winner: str) -> None:
        self.phase = Phase.END
        self.events.emit("game_over", winner)

    # ------------------------------------------------------------------
    # دسترسی به بازیکن
    # ------------------------------------------------------------------
    def _get_player(self, player_id: int) -> Player:
        for p in self.players:
            if p.id == player_id:
                return p
        raise PlayerNotFoundError(f"بازیکنی با شناسه {player_id} یافت نشد.")

    # ------------------------------------------------------------------
    # نماهای وضعیت (State Views)
    # ------------------------------------------------------------------
    def get_public_state(self) -> Dict[str, Any]:
        """نمای عمومی بازی (قابل ارسال به همه)."""
        return {
            "phase": self.phase.name.lower(),
            "round": self.round_number,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "alive": p.is_alive(),
                }
                for p in self.players
            ],
            "game_over": self.phase == Phase.END,
            "winner": getattr(self, "_winner", None) if self.phase == Phase.END else None,
        }

    def get_private_state(self, player_id: int) -> Dict[str, Any]:
        """نمای خصوصی یک بازیکن (اطلاعات محرمانهٔ او)."""
        player = self._get_player(player_id)
        state = self.get_public_state()
        state["my_role"] = player.role.name if player.role else "unknown"
        state["my_team"] = player.role.team if player.role else "unknown"
        # اطلاعات اختصاصی نقش
        if player.role:
            state["private_info"] = player.role.get_private_info(self, player)
        else:
            state["private_info"] = {}
        return state

    # ------------------------------------------------------------------
    # سریالایز کامل (ذخیره و بازیابی)
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """تمام وضعیت بازی را به یک دیکشنری سریالایز می‌کند."""
        import json
        return {
            "config": {
                "role_counts": self.config.role_counts,
                "max_players": self.config.max_players,
                "reveal_role_on_death": self.config.reveal_role_on_death,
            },
            "phase": self.phase.name.lower(),
            "round_number": self.round_number,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "alive": p.alive,
                    "role": p.role.name if p.role else None,
                    # وضعیت درونی نقش‌ها را هم ذخیره می‌کنیم (جادوگر، پزشک...)
                    "role_state": p.role.to_dict() if p.role else {},
                }
                for p in self.players
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Game":
        """بازی را از یک دیکشنری بازسازی می‌کند."""
        config = GameConfig(
            role_counts=data["config"]["role_counts"],
            max_players=data["config"]["max_players"],
            reveal_role_on_death=data["config"]["reveal_role_on_death"],
        )
        game = cls.__new__(cls)  # بدون صدا زدن __init__ عادی
        game.config = config
        game.events = GameEvents()
        game.players = []
        game.phase = Phase[data["phase"].upper()]
        game.round_number = data["round_number"]
        game._wolf_target_id = None
        game.night_manager = None
        game.day_manager = None

        from .roles import get_role_class
        for pdata in data["players"]:
            player = Player(pdata["id"], pdata["name"])
            player.alive = pdata["alive"]
            role_name = pdata["role"]
            if role_name:
                role_cls = get_role_class(role_name)
                role = role_cls.from_dict(pdata["role_state"]) if hasattr(role_cls, "from_dict") else role_cls()
                player.assign_role(role)
            game.players.append(player)
        return game