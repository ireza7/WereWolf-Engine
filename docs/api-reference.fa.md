# مرجع API

این بخش کلاس‌ها و توابع اصلی کتابخانهٔ werewolf را پوشش می‌دهد.

## Game

کلاس مرکزی که کل جریان بازی را مدیریت می‌کند.

### `Game(player_names, config=None)`
یک نمونهٔ جدید از بازی می‌سازد.

- `player_names` (لیستی از رشته‌ها): نام بازیکنان.
- `config` (GameConfig، اختیاری): پیکربندی بازی. اگر داده نشود، نقش‌ها باید دستی انتساب شوند.

### خصوصیات
- `players` (لیست Player): همهٔ بازیکنان.
- `phase` (Phase): فاز جاری بازی.
- `round_number` (int): دور جاری (بعد از `start()` عدد ۱ می‌شود).
- `events` (GameEvents): گذرگاه رویدادها.
- `night_manager` (NightManager یا None): مدیر شب (فقط در فاز NIGHT).
- `day_manager` (DayManager یا None): مدیر روز (فقط در فاز DAY).

### متدها
- `start()`: نقش‌ها را انتساب می‌دهد و اولین شب را شروع می‌کند.
- `night_action(actor_id, target_id)`: عملیات شبانهٔ بازیکن جاری را ثبت می‌کند.
- `night_skip(actor_id)`: نوبت بازیکن جاری را رد می‌کند (زمانی که هدف معتبری ندارد).
- `day_vote(voter_id, target_id)`: رأی یک بازیکن را ثبت می‌کند.
- `get_public_state()`: دیکشنری وضعیت عمومی بازی را برمی‌گرداند.
- `get_private_state(player_id)`: دیکشنری وضعیت خصوصی یک بازیکن را برمی‌گرداند.
- `to_dict()`: وضعیت کامل بازی را به یک دیکشنری سریالایز می‌کند.
- `from_dict(data)`: کلاس‌متد برای بازیابی بازی از یک دیکشنری.

## Player

نمایندهٔ یک بازیکن.

### `Player(player_id, name)`
- `id` (int): شناسهٔ یکتا.
- `name` (str): نام نمایشی.
- `alive` (bool): آیا بازیکن زنده است.
- `assign_role(role)`: یک نمونه نقش به بازیکن انتساب می‌دهد.
- `kill()`: بازیکن را می‌کشد (`alive` را `False` می‌کند).

## GameConfig

داده‌کلاس پیکربندی.

### `GameConfig(role_counts=None, max_players=20, reveal_role_on_death=False)`
- `role_counts` (dict[str, int]): نگاشت نام نقش به تعداد.
- `max_players` (int): حداکثر تعداد بازیکنان.
- `reveal_role_on_death` (bool): اگر `True` باشد، نقش فرد کشته‌شده عمومی می‌شود.

## Phase

Enum با مقادیر: `LOBBY`, `NIGHT`, `DAY`, `END`.

## GameEvents

گذرگاه رویداد ساده.

- `on(event_name, callback)`: یک callback برای یک رویداد ثبت می‌کند.
- `emit(event_name, *args, **kwargs)`: همهٔ handlerهای آن رویداد را صدا می‌زند.

## نقش‌ها

### BaseRole

کلاس انتزاعی پایه برای تمام نقش‌ها. رابط زیر را تعریف می‌کند (همه اختیاری برای بازنویسی):

- `name` (str): شناسهٔ نقش.
- `team` (str): `"village"`, `"werewolf"` یا تیم سفارشی.
- `night_priority` (int): اعداد کمتر زودتر عمل می‌کنند (مثلاً پیشگو ۱۰، گرگینه ۳۰).
- `can_act_night(game, player) -> bool`: آیا بازیکن امشب می‌تواند عمل کند.
- `get_available_targets(game, player) -> list[Player]`: لیست اهداف معتبر برای رابط کاربری.
- `perform_night_action(game, actor, target)`: اجرای عملیات شبانه.
- `get_private_info(game, player) -> dict`: اطلاعات خصوصی که فقط به آن بازیکن نشان داده می‌شود.
- `on_player_died(game, dead_player, cause)`: هوکی که وقتی هر بازیکنی می‌میرد صدا می‌شود.
- `on_vote_result(game, eliminated)`: هوکی که بعد از رأی‌گیری روز صدا می‌شود.

### رجیستری

- `register_role(name: str, role_cls: Type[BaseRole])`: یک کلاس نقش را ثبت می‌کند.
- `get_role_class(name: str) -> Type[BaseRole]`: کلاس یک نقش را برمی‌گرداند.
- `get_all_role_names() -> list[str]`: نام تمام نقش‌های ثبت‌شده را برمی‌گرداند.

## انواع خطا

- `WerewolfEngineError`: استثنای پایه.
- `InvalidActionError`: وقتی عملیات نامعتبر است.
- `NotYourTurnError`: وقتی نوبت بازیکن نیست.
- `GameNotStartedError`: وقتی عملیات قبل از شروع بازی صدا زده می‌شود.
- `GameOverError`: وقتی عملیات بعد از پایان بازی صدا زده می‌شود.
- `PlayerNotFoundError`: شناسهٔ بازیکن نامعتبر.
```