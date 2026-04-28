import pytest
from werewolf_engine.roles import Hunter, Villager, Werewolf


class TestHunter:
    def test_revenge_on_death(self, game):
        roles = [Hunter(), Villager(), Villager(), Villager(), Villager()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        hunter = game.players[0]
        victim = game.players[1]
        # کشتن شکارچی
        hunter.kill()
        game.events.on("player_killed", lambda p, c: None)  # جلوگیری از خطای نداشتن رویداد
        # شکارچی انتقام بگیرد
        hunter.role.on_player_died(game, hunter, cause="vote")
        # بررسی اینکه victim کشته شده
        assert not victim.alive

    def test_revenge_only_once(self, game):
        roles = [Hunter(), Villager(), Villager(), Villager(), Villager()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        hunter = game.players[0]
        hunter.kill()
        # اول
        hunter.role.on_player_died(game, hunter, cause="vote")
        dead_count = sum(1 for p in game.players if not p.alive)
        # یک نفر (شکارچی) + یک قربانی = ۲
        assert dead_count == 2
        # دومین بار نباید دوباره شلیک کند
        hunter.role.on_player_died(game, hunter, cause="vote")
        dead_count_2 = sum(1 for p in game.players if not p.alive)
        assert dead_count_2 == 2

    def test_no_revenge_if_protected(self, game):
        roles = [Hunter(), Villager(), Villager(), Villager(), Villager()]
        for p, r in zip(game.players, roles):
            p.assign_role(r)
        hunter = game.players[0]
        hunter.role.on_player_died(game, hunter, cause="protected")
        # هیچ‌کس جز شکارچی نباید بمیرد
        assert all(p.alive for p in game.players if p.id != hunter.id)