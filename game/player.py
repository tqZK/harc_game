import logging

from game.config import (COEF_LOGISTICS_TO_EXP, COEF_STRENGHT_TO_EXP, COEF_GOLD_TO_EXP, COEF_WAR_EXP_TO_EXP,
                         BASE_HIT_CHANCE, BASE_DEFENSE_CHANCE, BASE_FIRST_ATTACK_CHANCE, BASE_LIFE_POINTS)

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, player_id, strenght=0, logistics=0, gold=0):
        self.id = player_id
        self.strenght = strenght
        self.logistics = logistics
        self.gold = gold
        self.cumulative_gold = gold
        self.items = []
        self.war_exp = 0

        self.max_life_points = BASE_LIFE_POINTS

        self._life_points = self.max_life_points
        self.dmg_done = 0
        self.received_war_exp = 0

    @property
    def alive(self):
        return bool(self.life_points > 0)

    @property
    def life_points(self):
        return self._life_points

    @life_points.setter
    def life_points(self, value):
        self._life_points = max(0, value)

    @property
    def exp(self):
        return COEF_STRENGHT_TO_EXP * self.strenght + \
               COEF_LOGISTICS_TO_EXP * self.logistics + \
               COEF_GOLD_TO_EXP * self.cumulative_gold + \
               COEF_WAR_EXP_TO_EXP * self.war_exp

    @property
    def lvl(self):
        # TODO: dodefiniowac
        return self.exp // 1000 + 1

    @property
    def hit_chance(self):
        # ST
        # TODO: dodefiniowac
        # z wyliczen
        return round(self.lvl * self.hit_chance_buffs * 0.1 + BASE_HIT_CHANCE, 3)

    @property
    def defense_chance(self):
        # SO
        # TODO: dodefiniowac
        # z wyliczen
        return round(self.logistics * self.defense_chance_buffs * 0.01 + BASE_DEFENSE_CHANCE, 3)

    @property
    def first_attack_chance(self):
        # SO
        # TODO: dodefiniowac
        # z wyliczen
        return round(self.first_attack_chance_buffs + BASE_FIRST_ATTACK_CHANCE, 3)

    @property
    def hit_chance_buffs(self):
        # SP, inicjatywa
        # TODO: zalezy od przedmiotow i budynkow, zaimplementuj
        return 0.0

    @property
    def defense_chance_buffs(self):
        # TODO: zalezy od przedmiotow i budynkow, zaimplementuj
        return 0.0

    @property
    def first_attack_chance_buffs(self):
        # TODO: zalezy od przedmiotow i budynkow, zaimplementuj
        return 0.0

    def __str__(self):
        return f"Gracz {self.id}:\t" \
               f"lvl={self.lvl}\t" \
               f"sila={self.strenght}\t" \
               f"wikt_opierunek={self.logistics}\t" \
               f"zloto={self.gold}\t" \
               f"zloto_total={self.cumulative_gold}\t" \
               f"exp={self.exp}".expandtabs(11)

    def fight_stats(self):
        return f"Gracz {self.id}:\t" \
               f"lvl={self.lvl}\t" \
               f"punkty_zycia={self.life_points}\t" \
               f"max_punkty_zycia={self.max_life_points}\t" \
               f"sila={self.strenght}\t" \
               f"ST={self.hit_chance}\t" \
               f"SU={self.defense_chance}\t" \
               f"SP={self.first_attack_chance}\t".expandtabs(8)

    def reset_battle_results(self):
        self.dmg_done = 0
        self._life_points = self.max_life_points
        self.received_war_exp = 0
