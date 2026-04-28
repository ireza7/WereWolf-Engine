from werewolf_engine.roles import Doctor, Villager
from conftest import setup_night_game_with_roles


class TestDoctor:
    def test_can_act_night_true(self, game):
        roles = [Doctor(), Villager(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        doc = game.players[0]
        assert doc.role.can_act_night(game, doc) is True

    def test_cannot_protect_same_target_twice(self, game):
        roles = [Doctor(), Villager(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        doc = game.players[0]
        target = game.players[1]
        doc.role.perform_night_action(game, doc, target)
        doc.role._on_night_ended()
        available = doc.role.get_available_targets(game, doc)
        assert target not in available
        # پزشک می‌تواند خودش را هم محافظت کند، بنابراین ۴ نفر دیگر (Alice, Charlie, Diana, Eve)
        assert len(available) == 4

    def test_protection_sets_flag(self, game):
        roles = [Doctor(), Villager(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        doc = game.players[0]
        target = game.players[1]
        doc.role.perform_night_action(game, doc, target)
        assert target._protected is True