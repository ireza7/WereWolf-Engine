```markdown
# رویدادها

موتور بازی رویدادهایی منتشر می‌کند که می‌توانید با اتصال به آن‌ها رابط کاربری خود را به‌روز کنید.

## گوش دادن به رویدادها

```python
game.events.on("night_started", lambda round_num, actors: print(f"شب دور {round_num}"))
```

## مرجع رویدادها

| رویداد | آرگومان‌ها | توضیح |
|-------|-----------|-------------|
| `game_started` | `players` (لیست بازیکنان) | بازی شروع شده، نقش‌ها انتساب داده شده‌اند. |
| `night_started` | `round_number`، `actors` (لیست بازیکنان) | فاز شب آغاز می‌شود. `actors` کسانی هستند که می‌توانند عمل کنند. |
| `night_action` | `actor_id`، `target_id` | یک عملیات شبانه ثبت شد. |
| `day_started` | `round_number` | فاز روز آغاز می‌شود. |
| `vote_cast` | `voter_id`، `target_id` | یک رأی ثبت شد. |
| `player_killed` | `player` (بازیکن)، `cause` (علت) | یک بازیکن کشته شد. |
| `game_over` | `winner` (برنده) | بازی تمام شد. برنده می‌تواند `"village"`، `"werewolf"` یا یک تیم سفارشی باشد. |
```