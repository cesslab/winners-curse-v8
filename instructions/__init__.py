from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    ExperimentSubSession,
)

from .constants import Constants


from .views import Instructions

doc = """
Instructions
"""


def creating_session(subsession):
    pass


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    pass


page_sequence = [Instructions]
