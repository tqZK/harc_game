import configparser
from simulation.battle_simulation import simulate_battle


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read_file(open("simulation/config.ini"))
    config = config["battle"]

    n_battles = int(config["N_BATTLES"])
    results = []
    for _ in range(n_battles):
        results.append(simulate_battle(config).result)

    print(f"Zasymulowano {n_battles} bitew, z czego wygrano {sum(results)} ({sum(results) * 100 / n_battles}%)")
