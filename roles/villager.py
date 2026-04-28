from .base import BaseRole

class Villager(BaseRole):
    name = "villager"
    team = "village"
    night_priority = 0   # هرگز صدا زده نمی‌شود