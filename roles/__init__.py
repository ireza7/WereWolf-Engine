from typing import Dict, Type
from .base import BaseRole

# دفتر ثبت جهانی نقش‌ها
_role_registry: Dict[str, Type[BaseRole]] = {}


def register_role(name: str, role_cls: Type[BaseRole]) -> None:
    _role_registry[name] = role_cls


def get_role_class(name: str) -> Type[BaseRole]:
    if name not in _role_registry:
        raise KeyError(f"نقش '{name}' پیدا نشد. نقش‌های موجود: {list(_role_registry.keys())}")
    return _role_registry[name]


def get_all_role_names() -> list:
    return list(_role_registry.keys())


# ------------------------------------------------------------------
# ثبت نقش‌های اصلی (با ایمپورت خودکار)
# ------------------------------------------------------------------
from .villager import Villager
from .seer import Seer
from .doctor import Doctor
from .werewolf import Werewolf
from .hunter import Hunter
from .witch import Witch

register_role(Villager.name, Villager)
register_role(Seer.name, Seer)
register_role(Doctor.name, Doctor)
register_role(Werewolf.name, Werewolf)
register_role(Hunter.name, Hunter)
register_role(Witch.name, Witch)