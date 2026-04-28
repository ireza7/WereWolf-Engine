from ..roles.base import BaseRole
from ..player import Player
from ..errors import InvalidActionError, NotYourTurnError
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game

class NightManager:
    """هماهنگ‌کنندهٔ عملیات شبانه و حل تعارضات."""

    def __init__(self, game: "Game"):
        self.game = game
        # لیست مرتب‌شدهٔ بازیکنانی که امشب باید عمل کنند
        ordered = []
        for p in game.players:
            if p.is_alive() and p.role and p.role.can_act_night(game, p):
                ordered.append(p)
        ordered.sort(key=lambda p: p.role.night_priority)
        self._actors = ordered
        self._current_index = 0
        # رکورد موقت برای اجرا
        game._wolf_target_id = None
        # پرچم‌های شبانه را ریست کن
        for p in game.players:
            p._protected = False

    @property
    def current_actor(self) -> Optional[Player]:
        """بازیکنی که الان نوبت اوست که عمل کند."""
        if self._current_index < len(self._actors):
            return self._actors[self._current_index]
        return None

    def get_available_targets(self, player: Player) -> List[Player]:
        """اهداف قابل انتخاب برای بازیکن جاری."""
        return player.role.get_available_targets(self.game, player)

    def submit_action(self, actor_id: int, target_id: int) -> None:
        """
        ثبت عملیات شبانهٔ یک بازیکن.
        اگر بازیکن جاری نباشد خطا می‌دهد.
        """
        current = self.current_actor
        if current is None:
            raise NotYourTurnError("همه بازیکنان شب عمل کرده‌اند.")
        if current.id != actor_id:
            raise NotYourTurnError(f"نوبت بازیکن {current.name} است، نه شما.")

        target = self.game._get_player(target_id)  # متدی که بعداً در Game می‌سازیم
        available = self.get_available_targets(current)
        if target not in available:
            raise InvalidActionError("هدف نامعتبر است.")

        # اجرای عملیات نقش
        current.role.perform_night_action(self.game, current, target)
        # رفتن به نفر بعدی
        self._current_index += 1

    def all_actions_submitted(self) -> bool:
        """آیا همهٔ بازیکنانِ دارای عمل شبانه، عمل خود را انجام داده‌اند؟"""
        return self._current_index >= len(self._actors)

    def resolve(self) -> None:
        """
        بعد از ثبت تمام عملیات:
        - تعیین قربانی‌های واقعی با در نظر گرفتن طبیب و جادوگر
        - کشتن بازیکنان
        - انتشار رویدادهای مرگ
        """
        # ۱. جمع‌آوری منابع کشنده
        kills: List[tuple] = []  # (target, cause)

        wolf_target_id = getattr(self.game, '_wolf_target_id', None)
        if wolf_target_id is not None:
            wolf_target = self.game._get_player(wolf_target_id)
            if wolf_target.is_alive():
                kills.append((wolf_target, "werewolf"))

        # جادوگر: هدف کشتن
        for p in self.game.players:
            if p.is_alive() and isinstance(p.role, BaseRole) and p.role.name == "witch":
                witch = p.role
                kill_id = getattr(witch, '_kill_target_id', None)
                if kill_id is not None:
                    target = self.game._get_player(kill_id)
                    if target.is_alive():
                        kills.append((target, "witch"))

        # ۲. لیست بازیکنان محافظت‌شده (طبیب و معجون حیات)
        saved: set = set()
        # طبیب
        for p in self.game.players:
            if p._protected:
                saved.add(p.id)
        # جادوگر: معجون حیات
        for p in self.game.players:
            if p.is_alive() and isinstance(p.role, BaseRole) and p.role.name == "witch":
                heal_id = getattr(p.role, '_heal_target_id', None)
                if heal_id is not None:
                    saved.add(heal_id)

        # ۳. حذف کشته‌های محافظت‌شده
        final_kills = [(target, cause) for target, cause in kills if target.id not in saved]

        # ۴. اعمال مرگ
        for target, cause in final_kills:
            target.kill()
            self.game.events.emit("player_killed", target, cause=cause)

        # ۵. ریست وضعیت شبانه نقش‌ها (مثل پزشک و جادوگر)
        for p in self.game.players:
            if p.role and hasattr(p.role, '_on_night_ended'):
                p.role._on_night_ended()
        # ریست پرچم
        self.game._wolf_target_id = None