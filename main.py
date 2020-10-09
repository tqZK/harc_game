import argparse
import configparser
import logging
from simulation.battle_simulation import simulate_battle

logger = logging.getLogger(__name__)

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

    config = configparser.ConfigParser()
    config.read_file(open("simulation/config.ini"))
    config = config["battle"]

    n_battles = int(config["N_BATTLES"])
    results = []
    for _ in range(n_battles):
        results.append(simulate_battle(config).result)

    logger.info(f"Zasymulowano {n_battles} bitew, z czego wygrano {sum(results)} ({sum(results) * 100 / n_battles}%)")
