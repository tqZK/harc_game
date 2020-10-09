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
        logger.info("")
        logger.info("")
        logger.info("")
        logger.info("")
        logger.info("")
        logger.info("")
        self.results.result = result
        self.results.calculate_results(self.players, self.monsters)
        self.calculate_received_war_exp()

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
        player.battle_n_fights += 1

        if calculate_sucess(player.first_attack_chance):
            fight_results.player_attacked_first = True
            player.battle_attacked_first += 1
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
        player.battle_attacked += 1
        if calculate_sucess(player.hit_chance):
            monster.life_points -= player.dmg
            player.battle_dmg_done += player.dmg
            logger.info(f"{player.name} trafił Nieosłoniętego z wartością {player.dmg}. "
                        f"Pozostale punkty życia Nieosłoniętego: {monster.life_points}")
            fight_results.player_hit = True
            player.battle_hit += 1
            if not monster.alive:
                logger.info("Nieosłonięty zginął")
                fight_results.monster_died = True
                return False
        else:
            logger.info(f"{player.name} nie trafił.")
        return True

    @staticmethod
    def monster_attacks(player, monster, fight_results):
        logger.info(f"Nieosłonięty atakuje gracza o ksywie {player.name}.")
        fight_results.monster_attacked = True
        player.battle_was_attacked += 1
        if calculate_sucess(player.defense_chance):
            logger.info(f"{player.name} obronił się.")
            fight_results.player_defended = True
            player.battle_defended += 1
        else:
            player.life_points -= monster.strenght
            player.battle_received_dmg += monster.strenght
            logger.info(f"{player.name} nie obronił się i Nieosłonięty zaatakował z wartością {monster.strenght}. "
                        f"Pozostałe punkty życia gracza o ksywie {player.name}: {player.life_points}")
            if not player.alive:
                logger.info(f"{player.name} zemdlał.")
                fight_results.player_died = True
                return False
        return True

    def calculate_received_war_exp(self):
        logger.info(f"Wynik bitwy: {'wygrana' if self.results.result else 'przegrana'}")
        logger.info(f"W bitwie walczyło {len(self.players)} graczy oraz {len(self.monsters)} Nieosłoniętych.")
        if self.results.result:
            logger.info(f"{len([player for player in self.players if player.alive])} graczy przetrwało bitwę.")
        else:
            logger.info(f"{len([monster for monster in self.monsters if monster.alive])} Nieosłoniętych przetrwało bitwę.")
        logger.info(f"Gracze zadali łącznie {sum([player.battle_dmg_done for player in self.players])} obrażeń.")
        logger.info(f"Nieosłonięci zadali łącznie {sum([player.battle_received_dmg for player in self.players])} obrażeń.")

        received = []
        for player in self.players:
            left_life_points_percent = round(player.life_points * 100 / player.max_life_points, 2)
            player.received_war_exp = round(
                player.battle_dmg_done * max(left_life_points_percent, 10) / 100 * (1.0 + player.gained_war_exp_buff)
            )
            received.append(player.received_war_exp)
            logger.info(player.fight_stats())
            received_war_exp_info = f", \tma buff {player.gained_war_exp_buff} do otrzymywanego DB\t-\t" \
                                    f"otrzymuje {player.received_war_exp} DB" if self.results.result else ""

            logger.info(f"{player.name} "
                        f"brał udział w {player.battle_n_fights} walkach, "
                        f"zadał {player.battle_dmg_done} obrazeń, "
                        f"atakował pierwszy w {round(player.battle_attacked_first / (player.battle_attacked + 0.0000001) * 100)}% "
                        f"({player.battle_attacked_first}/{player.battle_attacked}) przypadków, "
                        f"trafił w {round(player.battle_hit / (player.battle_attacked + 0.0000001) * 100)}% "
                        f"({player.battle_hit}/{player.battle_attacked}) przypadków, "
                        f"obronił się w {round(player.battle_defended / (player.battle_was_attacked + 0.0000001) * 100)}% "
                        f"({player.battle_defended}/{player.battle_was_attacked}) przypadków, "
                        f"pozostało mu {player.life_points} punktów życia ({left_life_points_percent}%)\t"
                        f"{received_war_exp_info}")

        if self.results.result:
            logger.info(f"Średnia wartość otrzymanego DB: {(sum(received) / len(received))}")
            logger.info(f"Mediana wartości otrzymanego DB: {statistics.median(received)}")
            logger.info(f"Najmniejsza wartość otrzymanego DB: {min(received)}")
            logger.info(f"Najwieksza wartość otrzymanego DB: {max(received)}")
