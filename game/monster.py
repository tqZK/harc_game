import logging

from game.config import MONSTER_LIFE_RANDOMNESS, MOSTER_STRENGHT_RANDOMNESS
from game.utils import calculate_value_with_randomness

logger = logging.getLogger(__name__)


class Monster:
    def __init__(self, monster_id, lvl):
        self.id = monster_id
        self.lvl = lvl
        self._life_points = self.init_life_points()
        self.strenght = self.init_strenght()

    @property
    def life_points(self):
        return self._life_points

    @life_points.setter
    def life_points(self, value):
        self._life_points = max(0, value)

    def init_strenght(self):
        # TODO: dodefiniowac
        return calculate_value_with_randomness(self.lvl * 10, MOSTER_STRENGHT_RANDOMNESS)

    def init_life_points(self):
        # TODO: dodefiniowac
        return calculate_value_with_randomness(self.lvl * 100, MONSTER_LIFE_RANDOMNESS)

    @property
    def alive(self):
        return bool(self.life_points > 0)

    def __str__(self):
        return f"Potwor {self.id}:\t" \
               f"lvl={self.lvl}\t" \
               f"punkty_zycia={self.life_points}\t" \
               f"sila={self.strenght}".expandtabs(8)
