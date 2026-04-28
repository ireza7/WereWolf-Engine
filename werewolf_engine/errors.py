class WerewolfEngineError(Exception):
    """کلاس پایه برای تمام خطاهای کتابخانه."""
    pass


class InvalidActionError(WerewolfEngineError):
    """عملیات درخواستی معتبر نیست (هدف نامجاز، مرده و ...)."""
    pass


class NotYourTurnError(WerewolfEngineError):
    """بازیکن در این فاز یا مقطع حق انجام این عمل را ندارد."""
    pass


class GameNotStartedError(WerewolfEngineError):
    """بازی هنوز شروع نشده است."""
    pass


class GameOverError(WerewolfEngineError):
    """بازی تمام شده و نمی‌توان عملیات جدید انجام داد."""
    pass


class PlayerNotFoundError(WerewolfEngineError):
    """شناسهٔ بازیکن در بازی پیدا نشد."""
    pass