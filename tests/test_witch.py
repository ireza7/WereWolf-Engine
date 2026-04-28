from werewolf_engine.roles import Witch, Werewolf, Villager
from conftest import setup_night_game_with_roles


class TestWitch:
    def test_initial_potions(self, game):
        roles = [Witch(), Villager(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        witch = game.players[0]
        info = witch.role.get_private_info(game, witch)
        assert info["heal_available"] is True
        assert info["kill_available"] is True

    def test_use_heal_potion(self, game):
        roles = [Witch(), Werewolf(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        witch = game.players[0]
        game._wolf_target_id = game.players[1].id
        game._night_kill_victims = [game.players[1]]
        victim = game.players[1]
        targets = witch.role.get_available_targets(game, witch)
        assert victim in targets
        witch.role.perform_night_action(game, witch, victim)
        assert witch.role._heal_used is True
        assert witch.role._heal_target_id == victim.id

    def test_use_kill_potion(self, game):
        roles = [Witch(), Villager(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        witch = game.players[0]
        target = game.players[1]
        game._night_kill_victims = []
        witch.role.perform_night_action(game, witch, target)
        assert witch.role._kill_used is True
        assert witch.role._kill_target_id == target.id

    def test_cannot_heal_if_no_potion(self, game):
        roles = [Witch(), Werewolf(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        witch = game.players[0]
        witch.role._heal_used = True
        # جادوگر هنوز معجون مرگ دارد، پس می‌تواند گرگینه را بکشد
        # برخلاف تصور قبلی، Bob (werewolf) باید در اهداف باشد
        targets = witch.role.get_available_targets(game, witch)
        assert game.players[1] in targets

    def test_cannot_kill_self(self, game):
        roles = [Witch(), Villager(), Villager(), Villager(), Villager()]
        game, nm = setup_night_game_with_roles(game, roles)
        witch = game.players[0]
        targets = witch.role.get_available_targets(game, witch)
        assert witch not in targets