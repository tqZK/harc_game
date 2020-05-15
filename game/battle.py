import logging
import statistics
import random

from game.battle_results import BattleResults, RoundResults, FightResults
from game.utils import calculate_sucess

logger = logging.getLogger(__name__)


class Battle:
    def __init__(self, players=None, monsters=None):
        self.players = players or []
        self.monsters = monsters or []
        self.results = BattleResults()
        self.reset_player_stats()

    def reset_player_stats(self):
        for player in self.players:
            player.reset_battle_results()

    def run(self):
        round_id = 1
        while any([player.alive for player in self.players]) and any([monster.alive for monster in self.monsters]):
            logger.info(f">>> Runda {round_id}")
            self.roundx()
            round_id += 1

        if not any([player.alive for player in self.players]):
            result = 0
        else:
            result = 1

        logger.info(f">>>>> Bitwa {'wygrana' if result else 'przegrana'}")
        self.results.result = result
        self.results.calculate_results(self.players, self.monsters)
        self.calculate_received_war_exp(result)

    def roundx(self):
        round_results = RoundResults()

        players_alive = [player_set[0] for player_set in sorted(
            [(player, random.random()) for player in [player for player in self.players if player.alive]],
            key=lambda player: (player[0].lvl, player[0].strenght, player[0].logistics, player[1])
        )]
        monsters_alive = [monster_set[0] for monster_set in sorted(
            [(monster, random.random()) for monster in self.monsters if monster.alive],
            key=lambda monster: (monster[0].strenght, monster[0].life_points, monster[1])
        )]

        round_results.n_players = len(players_alive)
        round_results.n_monsters = len(monsters_alive)

        logger.info(f">>> Liczba żyjących graczy: {round_results.n_players}")
        logger.info(f">>> Liczba żyjących Nieosłoniętych: {round_results.n_monsters}")

        for player, monster in zip(players_alive, monsters_alive):
            round_results.fights.append(self.fight(player, monster))

        self.results.rounds.append(round_results)

    def fight(self, player, monster):
        fight_results = FightResults()

        logger.info(f">> Walka {player.name} z Nieosłoniętym numer {monster.monster_id}")
        logger.info(f">> {player.fight_stats()}")
        logger.info(f">> {monster}")

        if calculate_sucess(player.first_attack_chance):
            fight_results.player_attacked_first = True
            monster_survived = self.player_attacks(player, monster, fight_results)
            if monster_survived:
                self.monster_attacks(player, monster, fight_results)
        else:
            player_survived = self.monster_attacks(player, monster, fight_results)
            if player_survived:
                self.player_attacks(player, monster, fight_results)
        return fight_results

    @staticmethod
    def player_attacks(player, monster, fight_results):
        logger.info(f"{player.name} atakuje Nieosłoniętego.")
        fight_results.player_attacked = True
        if calculate_sucess(player.hit_chance):
            monster.life_points -= player.dmg
            player.dmg_done += player.dmg
            logger.info(f"{player.name} trafił Nieosłoniętego z wartością {player.dmg}. "
                        f"Pozostale punkty życia Nieosłoniętego: {monster.life_points}")
            fight_results.player_hit = True
            if not monster.alive:
                logger.info("Nieosłonięty zginal")
                fight_results.monster_died = True
                return False
        else:
            logger.info(f"{player.name} nie trafił.")
        return True

    @staticmethod
    def monster_attacks(player, monster, fight_results):
        logger.info(f"Nieosłonięty atakuje gracza o ksywie {player.name}.")
        fight_results.monster_attacked = True
        if calculate_sucess(player.defense_chance):
            logger.info(f"{player.name} obronił się.")
            fight_results.player_defended = True
        else:
            player.life_points -= monster.strenght
            logger.info(f"{player.name} nie obronił się i Nieosłonięty zaatakował z wartością {monster.strenght}. "
                        f"Pozostałe punkty życia gracza o ksywie {player.name}: {player.life_points}")
            if not player.alive:
                logger.info(f"{player.name} zemdlał.")
                fight_results.player_died = True
                return False
        return True

    def calculate_received_war_exp(self, result):
        received = []
        for player in self.players:
            left_life_points_percent = round(player.life_points * 100 / player.max_life_points, 2)
            player.received_war_exp = round(
                player.dmg_done * max(left_life_points_percent, 10) / 100 * (1.0 + player.gained_war_exp_buff)
            )
            received.append(player.received_war_exp)
            logger.info("---")
            logger.info(player.fight_stats())
            if result:
                logger.info(f"{player.name}:\t"
                            f"zadał {player.dmg_done} obrazen,\t"
                            f"pozostało mu {player.life_points} punktów życia ({left_life_points_percent}%)\t"
                            f"ma buff {player.gained_war_exp_buff} do otrzymywanego DB\t"
                            f"-\t"
                            f"otrzymuje {player.received_war_exp} DB")
            else:
                logger.info(f"{player.name}:\t"
                            f"zadał {player.dmg_done} obrazen,\t"
                            f"pozostało mu {player.life_points} punktów życia ({left_life_points_percent}%)\t")
        if result:
            print(f"Średnia wartość otrzymanego DB: {(sum(received) / len(received))}")
            print(f"Mediana wartosci otrzymanego DB: {statistics.median(received)}")
            print(f"Najmniejsza wartość otrzymanego DB: {min(received)}")
            print(f"Najwieksza wartość otrzymanego DB: {max(received)}")
