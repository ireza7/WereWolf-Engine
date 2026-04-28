import pytest
from werewolf_engine.roles import Villager
from werewolf_engine import Game, GameConfig
from werewolf_engine.phases import Phase
from werewolf_engine.phases.day import DayManager


class TestDayVoting:
    @pytest.fixture
    def day_game(self):
        player_names = ["A", "B", "C", "D", "E"]
        config = GameConfig(role_counts={})
        game = Game(player_names, config)
        for p in game.players:
            p.assign_role(Villager())
        game.phase = Phase.DAY
        dm = DayManager(game)
        game.day_manager = dm
        return game, dm

    def test_simple_majority(self, day_game):
        game, dm = day_game
        # همه به B رأی می‌دهند، B هم رأی می‌دهد
        dm.cast_vote(0, 1)  # A -> B
        dm.cast_vote(1, 0)  # B -> A
        dm.cast_vote(2, 1)  # C -> B
        dm.cast_vote(3, 1)  # D -> B
        dm.cast_vote(4, 1)  # E -> B
        eliminated = dm.resolve()
        assert eliminated is not None
        assert eliminated.id == 1
        assert not game.players[1].alive

    def test_tie_no_elimination(self, day_game):
        game, dm = day_game
        # A -> B, B -> C, C -> B, D -> C, E -> D
        dm.cast_vote(0, 1)  # A -> B
        dm.cast_vote(1, 2)  # B -> C
        dm.cast_vote(2, 1)  # C -> B
        dm.cast_vote(3, 2)  # D -> C
        dm.cast_vote(4, 3)  # E -> D
        eliminated = dm.resolve()
        assert eliminated is None
        assert all(p.alive for p in game.players)