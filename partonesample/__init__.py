from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    ExperimentSubSession,
)

from .views import (
    InstructionsPage, Bid, BestGuessLeft, BestGuessRight, Interval, Outcome, Summary, Payoff
)
from .constants import Constants

doc = """
Part I (Walkthrough)
"""


def creating_session(subsession):
    for player in subsession.get_players():
        player.treatment = player.session_treatment


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    min_guess = models.IntegerField(min=0, max=100)
    max_guess = models.IntegerField(min=0, max=100)
    guess = models.IntegerField(min=0, max=100)
    bid = models.IntegerField(min=0, max=100)
    is_payment_round = models.BooleanField(initial=False)
    # Bid History
    bid_history_id = models.IntegerField(initial=0)
    previous_session_id = models.IntegerField(initial=0)
    lottery_id = models.IntegerField(initial=1)
    treatment = models.StringField(choices=["cp", "cv"])
    lottery_round_number = models.IntegerField(initial=1)
    lottery_order = models.IntegerField(initial=1)
    others_group_id = models.IntegerField(initial=1)
    others_player_id = models.IntegerField(initial=1)
    signal = models.IntegerField(initial=22)
    signal1 = models.IntegerField()
    signal2 = models.IntegerField()
    signal3 = models.IntegerField()
    signal4 = models.IntegerField(initial=22)
    bid1 = models.IntegerField()
    bid2 = models.IntegerField()
    bid3 = models.IntegerField()
    bid4 = models.IntegerField()
    player_id = models.IntegerField()
    alpha = models.IntegerField(initial=10)
    beta = models.IntegerField(initial=30)
    epsilon = models.IntegerField(initial=4)
    ticket_value_before = models.IntegerField(initial=0)
    ticket_probability = models.IntegerField(initial=70)
    fixed_value = models.IntegerField(initial=70)
    ticket_value_after = models.IntegerField(initial=0)
    up_ticket = models.IntegerField(initial=20)
    # Player Bid History
    rounds_per_lottery = models.IntegerField(initial=1)
    player_bid_history_id = models.IntegerField(initial=0)
    part_round_number = models.IntegerField(initial=0)
    be_bid = models.FloatField(initial=0.0)


page_sequence = [InstructionsPage, BestGuessLeft, Outcome, BestGuessRight, Interval, Summary, Payoff]
