from typing import Callable, Dict, List


class GameEvents:
    """
    یک گذرگاه رویداد (Event Bus) ساده برای اتصال کتابخانه به دنیای بیرون.

    مصرف‌کننده می‌تواند با متد `on` یک تابع برای یک رویداد ثبت کند.
    کتابخانه با `emit` آن رویداد را به همراه پارامترها صدا می‌زند.
    """

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, callback: Callable) -> None:
        """یک handler برای رویداد `event_name` ثبت کن."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(callback)

    def emit(self, event_name: str, *args, **kwargs) -> None:
        """همهٔ handlerهای `event_name` را صدا بزن."""
        for handler in self._handlers.get(event_name, []):
            handler(*args, **kwargs)