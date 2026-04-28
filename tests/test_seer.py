from werewolf_engine.roles import Seer, Villager, Werewolf
from conftest import setup_night_game_with_roles


class TestSeer:
    def setup_method(self):
        self.roles = [Seer(), Villager(), Villager(), Villager(), Villager()]

    def test_can_act_night_always_true(self, game):
        game, nm = setup_night_game_with_roles(game, self.roles)
        seer = game.players[0]
        assert seer.role.can_act_night(game, seer) is True

    def test_available_targets_all_alive(self, game):
        game, nm = setup_night_game_with_roles(game, self.roles)
        seer = game.players[0]
        targets = seer.role.get_available_targets(game, seer)
        assert len(targets) == 5

    def test_available_targets_include_self(self, game):
        game, nm = setup_night_game_with_roles(game, self.roles)
        seer = game.players[0]
        targets = seer.role.get_available_targets(game, seer)
        assert seer in targets

    def test_perform_night_action_werewolf(self, game):
        roles = [Seer(), Werewolf(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        seer = game.players[0]
        werewolf = game.players[1]
        seer.role.perform_night_action(game, seer, werewolf)
        info = seer.role.get_private_info(game, seer)
        assert info["seer_last_result"]["result"] == "werewolf"

    def test_perform_night_action_not_werewolf(self, game):
        roles = [Seer(), Villager(), Werewolf(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        seer = game.players[0]
        villager = game.players[1]
        seer.role.perform_night_action(game, seer, villager)
        info = seer.role.get_private_info(game, seer)
        assert info["seer_last_result"]["result"] == "not werewolf"