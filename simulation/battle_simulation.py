from game.battle import Battle
from game.guild import Guild
from game.player import Player
from game.monster import Monster
from game.utils import calculate_value_with_randomness


def simulate_battle(config):
    guild = Guild()
    guild.players = [
        Player(
            player_id=n + 1,
            strenght=calculate_value_with_randomness(
                float(config["PLAYER_STRENGHT"]), float(config["PLAYER_STRENGHT_RANDOMNESS"])
            ),
            logistics=calculate_value_with_randomness(
                float(config["PLAYER_LOGISTICS"]), float(config["PLAYER_LOGISTICS_RANDOMNESS"])
            ),
            gold=calculate_value_with_randomness(
                float(config["PLAYER_GOLD"]), float(config["PLAYER_GOLD_RANDOMNESS"])
            )
        ) for n in range(int(config["N_PLAYERS"]))
    ]

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

    battle = Battle(guild.players, monsters)
    battle.run()

    battle.results.print_results()
    print()
    print('------------------------')
    print()
    return battle.results
