from otree.api import BaseConstants


class Constants(BaseConstants):
    name_in_url = "partone"
    players_per_group = None
    NUM_QUESTIONS = 3
    PART_NUMBER = 2
    PART_ONE = 1
    MIN_VALUATION = 0
    MAX_VALUATION = 100
    PREFIX = 'part_one_lottery_'
    NUM_LOTTERIES = 4
    ROUNDS_PER_LOTTERY = 3
    num_rounds = NUM_LOTTERIES * ROUNDS_PER_LOTTERY
