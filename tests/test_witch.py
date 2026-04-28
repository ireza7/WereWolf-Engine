import pytest
from werewolf_engine.roles import Witch, Werewolf, Villager


class TestWitch:
    def test_initial_potions(self, night_game):
        roles = [Witch(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        witch = game.players[0]
        info = witch.role.get_private_info(game, witch)
        assert info["heal_available"] is True
        assert info["kill_available"] is True

    def test_use_heal_potion(self, night_game):
        roles = [Witch(), Werewolf(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        witch = game.players[0]
        # شبیه‌سازی یک شکار توسط گرگینه
        game._wolf_target_id = game.players[1].id
        game._night_kill_victims = [game.players[1]]

        # جادوگر هدف نجات را انتخاب کند
        victim = game.players[1]
        # باید victim جزو available_targets باشد
        targets = witch.role.get_available_targets(game, witch)
        assert victim in targets

        witch.role.perform_night_action(game, witch, victim)  # نجات
        assert witch.role._heal_used is True
        assert witch.role._heal_target_id == victim.id

    def test_use_kill_potion(self, night_game):
        roles = [Witch(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        witch = game.players[0]
        target = game.players[1]
        # برای کشتن، باید قربانی شب مشخص نباشد (تا در لیست نباشد)
        game._night_kill_victims = []  # کسی امشب کشته نمی‌شود
        witch.role.perform_night_action(game, witch, target)  # کشتن
        assert witch.role._kill_used is True
        assert witch.role._kill_target_id == target.id

    def test_cannot_heal_if_no_potion(self, night_game):
        roles = [Witch(), Werewolf(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        witch = game.players[0]
        witch.role._heal_used = True
        targets = witch.role.get_available_targets(game, witch)
        # فقط باید از معجون کشتن بتواند استفاده کند
        assert game.players[1] not in targets  # victim شکار نباشد
        # اما می‌تواند کسی را بکشد
        assert any(p.id != game.players[1].id for p in targets)

    def test_cannot_kill_self(self, night_game):
        roles = [Witch(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        witch = game.players[0]
        targets = witch.role.get_available_targets(game, witch)
        assert witch not in targets