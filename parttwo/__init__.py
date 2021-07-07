import random

from otree.api import BaseGroup, BaseSubsession, models, BasePlayer, widgets

from exp.models import (
    BidHistoryPlayer,
    save_bid_history_for_all_players,
    ExperimentSubSession,
    create_player_bid_histories,
)

from exp.db import Phase, close_db

from .views import (
    Choice, Outcome
)
from .constants import Constants

doc = """
Choice Phase
"""


def creating_session(subsession):
    if subsession.round_number == 1:
        create_player_bid_histories(
            subsession.get_treatment_code(),
            subsession.get_players(),
            subsession.get_lottery_ids(Constants.NUM_LOTTERIES, Constants.PREFIX),
            subsession.session_id,
            Constants.ROUNDS_PER_LOTTERY,
            Phase.QUESTION_PHASE)

        for player in subsession.get_players():
            player.participant.vars['choice_payoff_lottery'] = random.randint(1, Constants.NUM_LOTTERIES)
            player.participant.vars['choice_payoff_round'] = random.randint(1, Constants.ROUNDS_PER_LOTTERY)

    save_bid_history_for_all_players(subsession.get_players(), Constants.ROUNDS_PER_LOTTERY, Phase.QUESTION_PHASE)
    close_db()


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    strategy_choice = models.IntegerField(
        choices=[
            [1, "Bid slightly below the average lottery payoff"],
            [2, "Bid slightly above the highest bid of the other three bidders"],
            [3, "Either is fine"]],
        widget=widgets.RadioSelectHorizontal
    )
    is_payment_round = models.BooleanField(initial=False)
    tie = models.BooleanField(initial=False)
    win_tie_break = models.BooleanField(initial=False)
    winner = models.BooleanField(initial=False)
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
    # Player Bid History
    rounds_per_lottery = models.IntegerField()
    player_bid_history_id = models.IntegerField()
    part_round_number = models.IntegerField()
    be_bid = models.FloatField()


page_sequence = [Choice, Outcome]
