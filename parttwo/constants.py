from otree.api import BaseConstants

from partone.constants import Constants as PartOneConstants

class Constants(BaseConstants):
    name_in_url = "parttwo"
    players_per_group = None
    NUM_QUESTIONS = 3
    PART_NUMBER = 2
    MIN_VALUATION = 0
    MAX_VALUATION = 100
    NUM_LOTTERIES = PartOneConstants.NUM_LOTTERIES
    ROUNDS_PER_LOTTERY = PartOneConstants.ROUNDS_PER_LOTTERY
    num_rounds = NUM_LOTTERIES * ROUNDS_PER_LOTTERY
