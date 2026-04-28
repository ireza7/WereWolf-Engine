import pytest
from werewolf_engine import Game, GameConfig
from werewolf_engine.phases import Phase
from werewolf_engine.phases.night import NightManager


@pytest.fixture
def game():
    """یک بازی پایه با ۵ بازیکن بدون نقش."""
    player_names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    config = GameConfig(role_counts={})
    game = Game(player_names, config)
    return game


def setup_night_game_with_roles(game, roles):
    """
    بازی را با نقش‌های داده‌شده تنظیم کرده و مدیر شب را برمی‌گرداند.
    roles: لیستی از نمونه‌های Role به ترتیب بازیکنان.
    """
    for player, role in zip(game.players, roles):
        player.assign_role(role)
    game.phase = Phase.NIGHT
    game._wolf_target_id = None
    game._night_kill_victims = []
    nm = NightManager(game)
    game.night_manager = nm
    return game, nm