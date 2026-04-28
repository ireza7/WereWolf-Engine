import pytest
from werewolf_engine import Game, GameConfig
from werewolf_engine.phases import Phase
from werewolf_engine.phases.night import NightManager
from werewolf_engine.roles import Werewolf, Villager, Doctor, Seer


class TestNightResolve:
    @pytest.fixture
    def setup(self, game):
        # نقش‌ها: گرگینه، پزشک، روستایی، روستایی، پیشگو
        roles = [Werewolf(), Doctor(), Villager(), Villager(), Seer()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        game.phase = Phase.NIGHT
        game._wolf_target_id = None
        game._night_kill_victims = []
        nm = NightManager(game)
        game.night_manager = nm
        return game, nm

    def test_doctor_protects_victim(self, setup):
        game, nm = setup
        wolf = game.players[0]
        doc = game.players[1]
        victim = game.players[2]
        # گرگینه شکار می‌کند
        wolf.role.perform_night_action(game, wolf, victim)
        # پزشک از همان قربانی محافظت می‌کند
        doc.role.perform_night_action(game, doc, victim)
        # پایان شب
        nm.resolve()
        assert victim.alive  # نباید مرده باشد

    def test_werewolf_kill_without_protection(self, setup):
        game, nm = setup
        wolf = game.players[0]
        victim = game.players[2]
        wolf.role.perform_night_action(game, wolf, victim)
        nm.resolve()
        assert not victim.alive