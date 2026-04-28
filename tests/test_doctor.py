import pytest
from werewolf_engine.roles import Doctor, Villager, Werewolf


class TestDoctor:
    def test_can_act_night_true(self, night_game):
        roles = [Doctor(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        doc = game.players[0]
        assert doc.role.can_act_night(game, doc) is True

    def test_cannot_protect_same_target_twice(self, night_game):
        roles = [Doctor(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        doc = game.players[0]
        target = game.players[1]

        # شب اول
        doc.role.perform_night_action(game, doc, target)
        doc.role._on_night_ended()
        # شب دوم (هنوز _last_protected_id = target.id)
        # برای تست، باید یک شب جدید بسازیم، ولی در اینجا ساده‌سازی می‌کنیم
        # فقط متد get_available_targets را چک می‌کنیم
        available = doc.role.get_available_targets(game, doc)
        assert target not in available
        # مطمئن شویم که بقیه هستند
        assert len(available) == 3  # ۴ بازیکن دیگر غیر از خودش و target

    def test_protection_sets_flag(self, night_game):
        roles = [Doctor(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        doc = game.players[0]
        target = game.players[1]
        doc.role.perform_night_action(game, doc, target)
        assert target._protected is True