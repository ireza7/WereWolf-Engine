import pytest
from werewolf_engine.roles import Werewolf, Villager, Seer


class TestWerewolf:
    def test_can_act_night_true(self, night_game):
        roles = [Werewolf(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        wolf = game.players[0]
        assert wolf.role.can_act_night(game, wolf) is True

    def test_available_targets_exclude_wolves(self, night_game):
        roles = [Werewolf(), Werewolf(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        wolf1 = game.players[0]
        targets = wolf1.role.get_available_targets(game, wolf1)
        # فقط روستایی‌ها (اندیس ۲،۳،۴) باید باشند
        assert all(p.id in {2, 3, 4} for p in targets)
        assert len(targets) == 3

    def test_perform_night_action_sets_wolf_target(self, night_game):
        roles = [Werewolf(), Villager(), Villager(), Villager(), Villager()]
        game, nm = night_game(roles)
        wolf = game.players[0]
        target = game.players[1]
        wolf.role.perform_night_action(game, wolf, target)
        assert game._wolf_target_id == target.id
        assert game._night_kill_victims == [target]