import random

from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    save_bid_history_for_all_players,
    ExperimentSubSession,
    create_player_bid_histories,
)

from exp.db import Phase, close_db

from .views import (
    BestGuess,
    Interval,
    Instructions,
    Outcome
)
from .constants import Constants

doc = """
Part I
"""


def creating_session(subsession):
    print("executing create sessions for partone")
    print(f"lotteries={Constants.NUM_LOTTERIES}, rounds per lottery={Constants.ROUNDS_PER_LOTTERY}")
    if subsession.round_number == 1:
        create_player_bid_histories(
            subsession.get_treatment_code(),
            subsession.get_players(),
            subsession.get_lottery_ids(Constants.NUM_LOTTERIES, Constants.PREFIX),
            subsession.session_id,
            Constants.ROUNDS_PER_LOTTERY,
            Phase.GUESS_PHASE)

        for player in subsession.get_players():
            player.participant.vars['part_one_payoff_lottery'] = random.randint(1, Constants.NUM_LOTTERIES)
            player.participant.vars['part_one_payoff_round'] = random.randint(1, Constants.ROUNDS_PER_LOTTERY)
            player.participant.vars['guess'] = []
            player.participant.vars['min_guess'] = []
            player.participant.vars['max_guess'] = []

    save_bid_history_for_all_players(subsession.get_players(), Constants.ROUNDS_PER_LOTTERY, Phase.GUESS_PHASE)
    # close_db()


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    # Input
    min_guess = models.IntegerField(min=0, max=100)
    max_guess = models.IntegerField(min=0, max=100)
    guess = models.IntegerField(min=0, max=100)
    # Payoff
    earnings = models.IntegerField()
    is_payment_round = models.BooleanField(initial=False)
    prep_emin = models.FloatField()
    prep_emax = models.FloatField()
    computed_loss = models.FloatField()
    random_k = models.IntegerField()
    high_bid_within_interval = models.BooleanField()
    confidence_value = models.FloatField(initial=0.0)
    guess_earnings = models.FloatField()
    interval_earnings = models.FloatField()
    computed_value_non_zero = models.BooleanField()
    prob_k_greater_than_l = models.IntegerField()
    l_less_than_k = models.BooleanField()
    # Bid History
    bid_history_id = models.IntegerField()
    previous_session_id = models.IntegerField()
    lottery_id = models.IntegerField()
    treatment = models.StringField(choices=["cp", "cv"])
    lottery_round_number = models.IntegerField()
    lottery_order = models.IntegerField()
    others_group_id = models.IntegerField()
    others_player_id = models.IntegerField()
    signal = models.IntegerField()
    signal1 = models.IntegerField()
    signal2 = models.IntegerField()
    signal3 = models.IntegerField()
    signal4 = models.IntegerField()
    bid1 = models.IntegerField()
    bid2 = models.IntegerField()
    bid3 = models.IntegerField()
    bid4 = models.IntegerField()
    player_id = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    epsilon = models.IntegerField()
    ticket_value_before = models.IntegerField()
    ticket_probability = models.IntegerField()
    fixed_value = models.IntegerField()
    ticket_value_after = models.IntegerField()
    up_ticket = models.IntegerField()
    others_high_bid = models.IntegerField()
    # Player Bid History
    rounds_per_lottery = models.IntegerField()
    player_bid_history_id = models.IntegerField()
    part_round_number = models.IntegerField()
    be_bid = models.FloatField()


page_sequence = [Instructions, BestGuess, Interval]
