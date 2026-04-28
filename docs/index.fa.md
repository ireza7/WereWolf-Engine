```markdown
# موتور بازی گرگینه

**یک کتابخانهٔ پایتونی انعطاف‌پذیر و توسعه‌پذیر برای ساخت بازی‌های مافیا / گرگینه.**

بدون هیچ وابستگی به رابط کاربری خاص، ربات تلگرام، اپ تحت وب یا بازی کنسولی خود را بسازید.

## ویژگی‌ها

- 🎭 **۶ نقش اصلی:** روستایی، گرگینه، پیشگو، پزشک، جادوگر، شکارچی.
- 🔌 **سیستم افزونه‌ای نقش‌ها:** نقش‌های دلخواه را بدون تغییر کد اصلی ثبت کنید.
- 🌙 **چرخهٔ کامل شب و روز** با اولویت‌بندی عملیات شبانه و حل تعارض.
- 🗳️ **سیستم رأی‌گیری** با قاعدهٔ اکثریت و مدیریت تساوی.
- 📡 **گذرگاه رویداد:** با اتصال به رویدادها رابط کاربری خود را پیش ببرید.
- 💾 **ذخیره و بازیابی:** وضعیت کامل بازی را با `to_dict()` و `from_dict()` ذخیره و بازیابی کنید.
- ✅ **تست‌های کامل:** بیش از ۲۳ تست خودکار برای همهٔ نقش‌ها و فازها.

## مثال سریع

```python
from werewolf_engine import Game, GameConfig

config = GameConfig(role_counts={
    "villager": 3,
    "werewolf": 2,
    "seer": 1,
    "doctor": 1,
    "witch": 1,
    "hunter": 1,
})

game = Game(["Ali", "Babak", "Changiz", "Diana", "Ehsan", "Farhad", "Giti", "Hamed", "Iman"], config)
game.start()

# بازی را با رابط کاربری خود هدایت کنید
while game.phase != Phase.END:
    if game.phase == Phase.NIGHT:
        actor = game.night_manager.current_actor
        if actor:
            targets = game.night_manager.get_available_targets(actor)
            # دریافت انتخاب کاربر و سپس:
            game.night_action(actor.id, choice)
    # مدیریت رأی‌گیری روز نیز مشابه
```

برای راهنمایی کامل به بخش [شروع کار](getting-started.md) مراجعه کنید.
```