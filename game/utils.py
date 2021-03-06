from random import uniform, random
import configparser

config = configparser.ConfigParser()


def calculate_value_with_randomness(base, coef_randomness):
    return round(base * (1 + uniform(-coef_randomness, coef_randomness)))


def calculate_sucess(wartosc):
    return random() <= wartosc
