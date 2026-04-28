from typing import Dict, Optional, List, TYPE_CHECKING
from ..errors import InvalidActionError, NotYourTurnError

if TYPE_CHECKING:
    from ..game import Game
    from ..player import Player

class DayManager:
    """مدیریت فاز رأی‌گیری روز."""

    def __init__(self, game: "Game"):
        self.game = game
        self._votes: Dict[int, int] = {}  # voter_id -> target_id
        self._voters: List[Player] = [p for p in game.players if p.is_alive()]
        self._current_voter_index = 0

    @property
    def current_voter(self) -> Optional["Player"]:
        if self._current_voter_index < len(self._voters):
            return self._voters[self._current_voter_index]
        return None

    def cast_vote(self, voter_id: int, target_id: int) -> None:
        """ثبت رأی یک بازیکن."""
        voter = self.game._get_player(voter_id)
        if voter not in self._voters:
            raise NotYourTurnError("شما اجازه رأی دادن ندارید.")
        if self._current_voter_index >= len(self._voters) or self._voters[self._current_voter_index].id != voter_id:
            raise NotYourTurnError("نوبت شما نیست.")

        target = self.game._get_player(target_id)
        if not target.is_alive() or target.id == voter_id:
            raise InvalidActionError("هدف رأی نامعتبر است.")

        self._votes[voter_id] = target_id
        self._current_voter_index += 1

    def all_votes_submitted(self) -> bool:
        return self._current_voter_index >= len(self._voters)

    def resolve(self) -> Optional["Player"]:
        """
        شمارش آرا و حذف بازیکنی که بیشترین رأی را دارد.
        در صورت تساوی، هیچ‌کس حذف نمی‌شود.
        برمی‌گرداند: بازیکن حذف‌شده یا None
        """
        if not self.all_votes_submitted():
            return None

        # شمارش آرا برای هر هدف
        target_counts: Dict[int, int] = {}
        for target_id in self._votes.values():
            target_counts[target_id] = target_counts.get(target_id, 0) + 1

        if not target_counts:
            return None

        max_votes = max(target_counts.values())
        top_targets = [tid for tid, count in target_counts.items() if count == max_votes]

        if len(top_targets) > 1:
            # تساوی، حذف نمی‌شود
            return None

        eliminated_id = top_targets[0]
        eliminated = self.game._get_player(eliminated_id)
        eliminated.kill()
        self.game.events.emit("player_killed", eliminated, cause="vote")
        return eliminated