import logging

from game.config import (COEF_LOGISTICS_TO_EXP, COEF_STRENGHT_TO_EXP, COEF_GOLD_TO_EXP, COEF_WAR_EXP_TO_EXP,
                         BASE_HIT_CHANCE, EXP_TO_NEXT_LVLS, BASE_DMG, BASE_DEFENSE_CHANCE, BASE_FIRST_ATTACK_CHANCE, BASE_LIFE_POINTS)

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, **player_data):
        try:
            self.player_id = int(player_data["player_id"])
            self.strenght = int(player_data["strenght"])
            self.logistics = int(player_data["logistics"])
            self.gold = int(player_data["gold"])
        except KeyError as e:
            logger.error(f"Nie mozna zainicjalizowac gracza - nie podano statystyki {e}")
            raise

        self.name = player_data.get("name", "")
        self.initials = player_data.get("initials", "")

        self.war_exp = int(player_data.get("war_exp", 0))
        self.driver = (player_data.get("driver", "") == "tak")
        self.training_cich = (player_data.get("training_cich", "") == "tak")
        self.training_thh = (player_data.get("training_thh", "") == "tak")
        self.training_malk = (player_data.get("training_malk", "") == "tak")
        self.training_wig = (player_data.get("training_wig", "") == "tak")

        # TODO: this should be set only based on items?
        self.gained_gold_buff = float(player_data.get("gained_gold_buff", 0.0))
        self.gained_strength_buff = float(player_data.get("gained_strength_buff", 0.0))
        self.gained_logistics_buff = float(player_data.get("gained_logistics_buff", 0.0))
        self.gained_war_exp_buff = float(player_data.get("gained_war_exp_buff", 0.0))

        self.cumulative_gold = self.gold + int(player_data.get("gold_for_guild", 0)) + int(player_data.get("gold_for_private", 0))

        self.hit_chance_buffs = 0.0
        self.defense_chance_buffs = 0.0
        self.first_attack_chance_buffs = 0.0
        self.recon_chance_buffs = 0.0
        self.added_life_points = 0

        self.parse_items(player_data)

        logger.debug(f"Gracz {self.player_id} pomyslnie stworzony")

        self._life_points = self.max_life_points
        self.dmg_done = 0.0
        self.received_war_exp = 0

    @property
    def alive(self):
        return bool(self.life_points > 0)

    @property
    def max_life_points(self):
        return BASE_LIFE_POINTS + self.added_life_points

    @property
    def life_points(self):
        return self._life_points

    @life_points.setter
    def life_points(self, value):
        self._life_points = max(0, value)

    @property
    def dmg(self):
        return BASE_DMG + self.strenght * 0.1

    @property
    def exp(self):
        return round(COEF_STRENGHT_TO_EXP * self.strenght + \
               COEF_LOGISTICS_TO_EXP * self.logistics + \
               COEF_GOLD_TO_EXP * self.cumulative_gold + \
               COEF_WAR_EXP_TO_EXP * self.war_exp)

    @property
    def lvl(self):
        return 1 + next((k for k, value in enumerate(EXP_TO_NEXT_LVLS) if value > self.exp), 9)

    @property
    def hit_chance(self):
        # ST
        return round(BASE_HIT_CHANCE + self.lvl * 0.03 + self.hit_chance_buffs, 3)

    @property
    def defense_chance(self):
        # SO
        return round(BASE_DEFENSE_CHANCE + self.logistics * 0.0001 + self.defense_chance_buffs, 3)

    @property
    def first_attack_chance(self):
        # SP, inicjatywa
        return round(BASE_FIRST_ATTACK_CHANCE + self.first_attack_chance_buffs, 3)

    def parse_items(self, player_data):
        item_places = ["helmet", "armor", "hand_1", "hand_2", "other_1", "other_2"]
        for item_place in item_places:
            if item_place in player_data:
                item = player_data[item_place]
                for stat in item[1]:
                    setattr(self, stat[0], getattr(self, stat[0]) + stat[1])

    def __repr__(self):
        return f"<Gracz {self.player_id}>"

    def __str__(self):
        return f"Gracz {self.player_id}:\t" \
               f"lvl={self.lvl}\t" \
               f"sila={self.strenght}\t" \
               f"wikt_opierunek={self.logistics}\t" \
               f"zloto={self.gold}\t" \
               f"zloto_total={self.cumulative_gold}\t" \
               f"exp={self.exp}".expandtabs(11)

    def fight_stats(self):
        return f"Gracz {self.player_id}:\t" \
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
