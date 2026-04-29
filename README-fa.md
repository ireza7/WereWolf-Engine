<div dir="rtl">

# موتور بازی گرگینه

یک کتابخانهٔ پایتون انعطاف‌پذیر و توسعه‌پذیر برای بازی‌های مافیا / گرگینه.

[![Tests](https://github.com/ireza7/WereWolf-Engine/actions/workflows/tests.yml/badge.svg)](https://github.com/ireza7/WereWolf-Engine/actions)
[![PyPI version](https://badge.fury.io/py/werewolf-engine.svg)](https://pypi.org/project/werewolf-engine/)

## ویژگی‌ها

- ۶ نقش اصلی: روستایی، گرگینه، پیشگو، پزشک، جادوگر، شکارچی
- سیستم افزونه‌ای برای نقش‌های سفارشی
- چرخهٔ کامل شب و روز با اولویت‌بندی و حل تعارض
- سیستم رأی‌گیری با قاعدهٔ اکثریت و مدیریت تساوی
- گذرگاه رویداد برای یکپارچه‌سازی رابط کاربری
- ذخیره و بازیابی وضعیت بازی (به‌صورت دیکشنری)
- بیش از ۲۳ تست خودکار برای تمام ویژگی‌ها

## نصب

```bash
pip install werewolf-engine
```

## مثال سریع

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={"villager": 3, "werewolf": 2, "seer": 1, "doctor": 1, "witch": 1, "hunter": 1})
game = Game(["علی", "بابک", "چنگیز", "دیانا", "احسان", "فرهاد", "گیتی", "حامد", "ایمان"], config)
game.start()

# بازی را با رابط کاربری خود هدایت کنید
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        actor = game.night_manager.current_actor
        if actor:
            targets = game.night_manager.get_available_targets(actor)
            game.night_action(actor.id, chosen_target.id)
```

## مستندات

مستندات کامل به زبان **فارسی** و **انگلیسی** در [ویکی گیت‌هاب](https://github.com/ireza7/WereWolf-Engine/wiki) در دسترس است:

- [خانه](https://github.com/ireza7/WereWolf-Engine/wiki/Home-fa)
- [شروع کار](https://github.com/ireza7/WereWolf-Engine/wiki/Getting-Started-fa)
- [نقش‌ها](https://github.com/ireza7/WereWolf-Engine/wiki/Roles-fa)
- [رویدادها](https://github.com/ireza7/WereWolf-Engine/wiki/Events-fa)
- [مرجع API](https://github.com/ireza7/WereWolf-Engine/wiki/API-Reference-fa)
- [مشارکت](https://github.com/ireza7/WereWolf-Engine/wiki/Contributing-fa)

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.

</div>