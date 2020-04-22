import logging
logger = logging.getLogger(__name__)


class BattleResults:
    def __init__(self):
        self.result = ''
        self.rounds = []
        self.player = []
        self.monsters = []

        self.n_fights = 0
        self.n_rounds = 0
        self.battle_player_hit = 0
        self.battle_player_defened = 0
        self.battle_player_attacked = 0
        self.battle_monster_attacked = 0
        self.battle_player_attacked_first = 0
        self.n_gamers_per_round = []
        self.n_monsters_per_round = []

    def calculate_results(self, players, monsters):
        self.n_rounds = len(self.rounds)

        for roundx in self.rounds:
            self.n_gamers_per_round.append(roundx.n_players)
            self.n_monsters_per_round.append(roundx.n_monsters)
            self.n_fights += len(roundx.fights)

            for fight in roundx.fights:
                self.battle_player_hit += fight.player_hit
                self.battle_player_defened += fight.player_defended
                self.battle_player_attacked += fight.player_attacked
                self.battle_monster_attacked += fight.monster_attacked
                self.battle_player_attacked_first += fight.player_attacked_first

    def print_results(self):
        print(f"Wynik bitwy: {'wygrana' if self.result else 'przegrana'}")
        print(f"Liczba rund: {self.n_rounds}")
        print(f"Liczba walk: {self.n_fights}")
        print(f"Gracz atakowal (na bitwe): {self.battle_player_attacked}")
        print(f"Gracz trafil (na bitwe): {self.battle_player_hit}")
        print(f"Gracz trafil % (na bitwe): {round(self.battle_player_hit / self.battle_player_attacked, 3)}")
        print(f"Potwor atakowal (na bitwe): {self.battle_monster_attacked}")
        print(f"Gracz obronil (na bitwe): {self.battle_player_defened}")
        print(f"Gracz obronil % (na bitwe): {round(self.battle_player_defened / self.battle_monster_attacked, 3)}")

        print(f"Gracz atakowal pierwszy: {self.battle_player_attacked_first}")
        print(f"Gracz atakowal pierwszy % (na bitwe): {round(self.battle_player_attacked_first / self.n_fights, 3)}")


class RoundResults:
    def __init__(self):
        self.n_players = 0
        self.n_monsters = 0
        self.fights = []


class FightResults:
    def __init__(self):
        self.player_attacked = False
        self.player_hit = False
        self.monster_attacked = False
        self.player_defended = False
        self.monster_died = False
        self.player_died = False
        self.player_attacked_first = False
