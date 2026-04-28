```markdown
# شروع کار

## نصب

```bash
pip install werewolf-engine
```

برای نسخهٔ در حال توسعه:

```bash
git clone https://github.com/your-username/WereWolf-Engine
cd WereWolf-Engine
pip install -e ".[dev]"
```

## استفادهٔ پایه

### ۱. ساخت بازی

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={
    "villager": 3,
    "werewolf": 2,
    "seer": 1,
    "doctor": 1,
    "witch": 1,
    "hunter": 1
})

game = Game(["Ali", "Babak", "Changiz", "Diana", "Ehsan", "Farhad", "Giti", "Hamed", "Iman"], config)
```

### ۲. گوش دادن به رویدادها (اختیاری)

```python
game.events.on("game_started", lambda players: print("بازی شروع شد!"))
game.events.on("night_started", lambda round_num, actors: print(f"شب دور {round_num}"))
game.events.on("player_killed", lambda player, cause: print(f"{player.name} با علت {cause} کشته شد"))
game.events.on("game_over", lambda winner: print(f"برنده: {winner}"))
```

### ۳. شروع بازی

```python
game.start()
```

حالا بازی در فاز **شب** قرار دارد. باید بازیکنان دارای عملیات شبانه را از `game.night_manager` بگیرید و انتخاب‌هایشان را دریافت کنید.

### ۴. پیش‌بردن فاز شب

```python
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        nm = game.night_manager
        while not nm.all_actions_submitted():
            actor = nm.current_actor
            if actor:
                targets = nm.get_available_targets(actor)
                # از کاربر (یا هوش مصنوعی) هدف بگیرید
                chosen = get_user_choice(actor, targets)
                if chosen is not None:
                    game.night_action(actor.id, chosen.id)
                else:
                    game.night_skip(actor.id)   # اگر هدف معتبری ندارد
        # شب پس از آخرین عملیات به‌طور خودکار تمام می‌شود
```

### ۵. پیش‌بردن فاز روز

```python
    elif game.phase == Phase.DAY:
        dm = game.day_manager
        while not dm.all_votes_submitted():
            voter = dm.current_voter   # بسته به رابط کاربری شما
            # رأی کاربر را دریافت کنید
            target = get_vote(voter)
            game.day_vote(voter.id, target.id)
        # روز پس از ثبت همهٔ آرا تمام می‌شود
```

### ۶. دسترسی به وضعیت بازی

نمای عمومی برای همه:

```python
public = game.get_public_state()
# {"phase": "day", "round": 2, "players": [...], ...}
```

نمای خصوصی برای یک بازیکن خاص:

```python
private = game.get_private_state(player_id)
# {"my_role": "seer", "my_team": "village", "private_info": {...}}
```

### ۷. ذخیره و بازیابی

```python
data = game.to_dict()
# در پایگاه داده یا Redis ذخیره کنید ...

restored_game = Game.from_dict(data)
```

## گام‌های بعدی

- آشنایی با [نقش‌ها](roles.md).
- استفاده از [سیستم رویدادها](events.md) برای ساخت ربات.
- مشاهدهٔ [مرجع API](api-reference.md) برای جزئیات فنی.
```