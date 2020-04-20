import logging

from game.battle_results import BattleResults, RoundResults, FightResults
from game.utils import calculate_sucess

logger = logging.getLogger(__name__)


class Battle:
    def __init__(self, players=None, monsters=None):
        self.players = players or []
        self.monsters = monsters or []
        self.results = BattleResults()

    def run(self):
        round_id = 1
        while any([player.alive for player in self.players]) and any([monster.alive for monster in self.monsters]):
            logger.info(f">>> Runda {round_id}")
            self.roundx()
            round_id += 1

        if not any([player.alive for player in self.players]):
            result = "przegrana"
        else:
            result = "wygrana"

        logger.info(f">>>>> Bitwa {result}")
        self.results.result = result
        self.results.calculate_results(self.players, self.monsters)

    def roundx(self):
        round_results = RoundResults()

        players_alive = sorted(
            [player for player in self.players if player.alive],
            key=lambda player: (player.lvl, player.strenght, player.logistics)
        )
        monsters_alive = sorted(
            [monster for monster in self.monsters if monster.alive],
            key=lambda monster: (monster.lvl, monster.strenght)
        )

        round_results.n_players = len(players_alive)
        round_results.n_monsters = len(monsters_alive)

        logger.info(f">>> Liczba zyjacych graczy: {round_results.n_players}")
        logger.info(f">>> Liczba zyjacych potworow: {round_results.n_monsters}")

        for player, monster in zip(players_alive, monsters_alive):
            round_results.fights.append(self.fight(player, monster))

        self.results.rounds.append(round_results)

    def fight(self, player, monster):
        fight_results = FightResults()

        logger.info(f">> Walka gracza {player.id} z potworem {monster.id}")
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
        logger.info(f"Gracz atakuje potwora.")
        fight_results.player_attacked = True
        if calculate_sucess(player.hit_chance):
            monster.life_points -= player.strenght
            logger.info(f"Gracz trafil potwora z wartoscia {player.strenght}. "
                        f"Pozostale punkty zycia potwora: {monster.life_points}")
            fight_results.player_hit = True
            if not monster.alive:
                logger.info("Potwor zginal")
                fight_results.monster_died = True
                return False
        else:
            logger.info("Gracz nie trafil.")
        return True

    @staticmethod
    def monster_attacks(player, monster, fight_results):
        logger.info(f"Potwor atakuje gracza.")
        fight_results.monster_attacked = True
        if calculate_sucess(player.defense_chance):
            logger.info(f"Gracz obronil sie.")
            fight_results.player_defended = True
        else:
            player.life_points -= monster.strenght
            logger.info(f"Gracz nie obronil sie i potwor zaatakowal z wartoscia {monster.strenght}. "
                        f"Pozostale punkty zycia gracza: {player.life_points}")
            if not player.alive:
                logger.info("Gracz zemdlal.")
                fight_results.player_died = True
                return False
        return True
