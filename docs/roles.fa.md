```markdown
# نقش‌ها

موتور بازی با شش نقش پیش‌فرض عرضه می‌شود. شما می‌توانید نقش‌های دلخواه خود را اضافه کنید.

| نقش | تیم | عمل شبانه | ویژگی خاص |
|------|-----|-----------|------------|
| روستایی | روستا | ندارد | – |
| گرگینه | گرگینه | شکار یک غیرگرگینه | هم‌تیمی‌ها را می‌شناسد |
| پیشگو | روستا | استعلام یک بازیکن | نتیجه «گرگینه» یا «غیرگرگینه» |
| پزشک | روستا | محافظت از یک بازیکن | نمی‌تواند دو شب پشت سر هم از یک نفر محافظت کند |
| جادوگر | روستا | استفاده از دو معجون (حیات و مرگ) یک‌بار در بازی | معجون حیات می‌تواند قربانی امشب را نجات دهد؛ معجون مرگ هر بازیکن زنده‌ای را هدف قرار می‌دهد |
| شکارچی | روستا | ندارد | وقتی به هر علت کشته شود، یک بازیکن زنده را با خود می‌کشد |

## ساختن نقش دلخواه

۱. از `werewolf_engine.roles.base.BaseRole` ارث‌بری کنید.  
۲. متدهای مورد نیاز را بازنویسی کنید (`can_act_night`, `perform_night_action` و ...).  
۳. نقش را ثبت کنید:

```python
from werewolf_engine.roles import register_role, BaseRole

class Cupid(BaseRole):
    name = "cupid"
    team = "village"
    night_priority = 5

    def can_act_night(self, game, player):
        return True  # مثلاً فقط یک بار؟ خودتان تصمیم بگیرید

    def get_available_targets(self, game, player):
        return [p for p in game.players if p.is_alive()]

    def perform_night_action(self, game, actor, target):
        # منطق ویژهٔ شما
        pass

register_role("cupid", Cupid)
```

اکنون می‌توانید `"cupid"` را در `GameConfig.role_counts` استفاده کنید.

برای دیدن رابط کامل نقش، به [مرجع API](api-reference.md) مراجعه کنید.
```