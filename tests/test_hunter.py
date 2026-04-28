import pytest
from werewolf_engine.roles import Hunter, Villager
from werewolf_engine.roles import hunter as hunter_module


class TestHunter:
    def test_revenge_on_death(self, game, monkeypatch):
        roles = [Hunter(), Villager(), Villager(), Villager(), Villager()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        hunter = game.players[0]
        victim = game.players[1]  # باب

        # مجبور می‌کنیم random.choice قربانی مورد نظر ما را انتخاب کند
        monkeypatch.setattr(
            hunter_module.random, "choice", lambda lst: [p for p in lst if p.id == victim.id][0]
        )

        hunter.kill()
        game.events.on("player_killed", lambda *args, **kwargs: None)
        hunter.role.on_player_died(game, hunter, cause="vote")
        assert not victim.alive

    def test_revenge_only_once(self, game):
        roles = [Hunter(), Villager(), Villager(), Villager(), Villager()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        hunter = game.players[0]
        hunter.kill()
        hunter.role.on_player_died(game, hunter, cause="vote")
        dead_count = sum(1 for p in game.players if not p.alive)
        assert dead_count == 2
        hunter.role.on_player_died(game, hunter, cause="vote")
        dead_count_2 = sum(1 for p in game.players if not p.alive)
        assert dead_count_2 == 2

    def test_no_revenge_if_protected(self, game):
        roles = [Hunter(), Villager(), Villager(), Villager(), Villager()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        hunter = game.players[0]
        hunter.role.on_player_died(game, hunter, cause="protected")
        assert all(p.alive for p in game.players if p.id != hunter.id)