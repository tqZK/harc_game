import argparse
import logging

from game.battle import Battle
from game.guild import Guild
from game.player import Player
from game.monster import Monster
from game.utils import calculate_value_with_randomness

N_BATTLES = 1

N_PLAYERS = 100
N_MONSTERS = int(N_PLAYERS * 1.2)

PLAYER_STRENGHT_RANDOMNESS = 0.2
PLAYER_LOGISTICS_RANDOMNESS = 0.2
PLAYER_GOLD_RANDOMNESS = 0.2

logger = logging.getLogger(__name__)


def simulate_battle():
    guild = Guild()
    guild.players = [
        Player(
            player_id=n + 1,
            strenght=calculate_value_with_randomness(10, PLAYER_STRENGHT_RANDOMNESS),
            logistics=calculate_value_with_randomness(10, PLAYER_LOGISTICS_RANDOMNESS),
            gold=calculate_value_with_randomness(10, PLAYER_GOLD_RANDOMNESS)
        ) for n in range(N_PLAYERS)
    ]
    # print(guild)

    monsters = [
        Monster(
            monster_id=n + 1,
            lvl=1
        ) for n in range(N_MONSTERS)]

    battle = Battle(guild.players, monsters)
    battle.run()
    battle.results.print_results()
    return battle.results.result is "wygrana"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Pokazuj informacje do debugowania",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Pokazuj wszystkie mozliwe informacje",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    results = []
    for _ in range(N_BATTLES):
        results.append(simulate_battle())

    print(sum(results))
