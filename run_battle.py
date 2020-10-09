from game.battle import Battle
from game.monster import Monster
from game.utils import calculate_value_with_randomness

from export.players_exporter import PlayersExporter
from export.guild_exporter import GuildExporter

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.root.setLevel(logging.NOTSET)
import configparser


def simulate_battle(config):
    # TODO: add saving log file
    guild_exporter = GuildExporter()
    guild_stats, guild_stats_for_player = guild_exporter.export_guild_tsv('real_data/BAZA_DANYCH - GILDIA.tsv')

    exporter = PlayersExporter(buffs_from_guild=guild_stats_for_player)
    players = exporter.export_players_tsv('real_data/BAZA_DANYCH - GRACZE.tsv')

    monsters = [
        Monster(
            monster_id=n + 1,
            strength=calculate_value_with_randomness(
                float(config["MONSTER_STRENGHT"]), float(config["MONSTER_STRENGHT_RANDOMNESS"])
            ),
            life_points=calculate_value_with_randomness(
                float(config["MONSTER_LIFE_POINTS"]), float(config["MONSTER_LIFE_RANDOMNESS"])
            ),
            first_attack_chance=0.5
        ) for n in range(int(config["N_MONSTERS"]))]

    battle = Battle(players, monsters)
    battle.run()
    battle.results.print_results()
    return battle.results


if __name__ == '__main__':


    config = configparser.ConfigParser()
    config.read_file(open("simulation/config.ini"))
    config = config["battle"]

    n_battles = int(config["N_BATTLES"])
    results = []
    for _ in range(n_battles):
        results.append(simulate_battle(config).result)

    print(f"Zasymulowano {n_battles} bitew, z czego wygrano {sum(results)} ({round(sum(results) * 100 / (n_battles + 0.0000001), 2)}%)")
