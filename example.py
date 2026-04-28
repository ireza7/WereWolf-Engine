import random
from werewolf_engine import Game, GameConfig, Phase

config = GameConfig(role_counts={
    "villager": 3,
    "seer": 1,
    "doctor": 1,
    "werewolf": 2,
    "witch": 1,
    "hunter": 1,
})

game = Game(["Ali", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy"], config)
game.events.on("game_started", lambda players: print("Game started!"))
game.events.on("night_started", lambda r, actors: print(f"Night {r}, actors: {[a.name for a in actors]}"))
game.events.on("player_killed", lambda player, cause: print(f"{player.name} died by {cause}"))
game.events.on("game_over", lambda winner: print(f"Winner: {winner}"))

game.start()

while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        nm = game.night_manager
        while nm and not nm.all_actions_submitted():
            actor = nm.current_actor
            targets = nm.get_available_targets(actor)
            if targets:
                target = random.choice(targets)
                game.night_action(actor.id, target.id)
                print(f"{actor.name} ({actor.role.name}) targets {target.name}")
            else:
                game.night_skip(actor.id)
                print(f"{actor.name} ({actor.role.name}) skips (no targets)")
    elif game.phase == Phase.DAY:
        dm = game.day_manager
        while dm and not dm.all_votes_submitted():
            voter = dm.current_voter
            alive = [p for p in game.players if p.is_alive() and p.id != voter.id]
            if alive:
                target = random.choice(alive)
                game.day_vote(voter.id, target.id)
                print(f"{voter.name} votes {target.name}")
            else:
                break

print("Final state:", game.get_public_state())