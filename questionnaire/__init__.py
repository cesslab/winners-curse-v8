from otree.api import *

from exp.models import (
    BidHistoryPlayer,
)

from .views import PartOne, PartTwo, PartThree
c = Currency


doc = """
Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    p1_q1 = models.StringField(label="Gender")
    p1_q2 = models.IntegerField(min=18, max=100, label="Age")
    p1_q3 = models.StringField(label="Major")

    p2_q1 = models.IntegerField(
        label='1. What object did you think about when you submitted your bid?',
        choices=[
            [1, 'The average worth of the lottery ticket given my signal'],
            [2, 'Only my signal'],
            [3, 'The worth of the lottery if I had the highest signal'],
            [4, 'The highest possible worth of the lottery'],
            [5, 'The lowest possible worth of the lottery'],
            [6, 'Other (Please specify)'],
        ],
        widget=widgets.RadioSelect
    )
    p2_q1_explain = models.LongStringField(label="Specify Other", blank=True)

    p2_q2 = models.LongStringField(
        label='2. What general bidding rule given a signal do you think other people followed in the experiment?')

    p2_q3 = models.IntegerField(min=0, max=100, label='')

    p2_q4 = models.IntegerField(
        label='4. Suppose that you could choose to play one of the following two lottery tickets. Which one would you prefer?',
        choices=[
            [1, 'I prefer lottery A'],
            [2, 'I prefer lottery B'],
            [3, "I don't care"],
        ],
        widget=widgets.RadioSelect
    )
    p2_q4_explain = models.LongStringField(label="Explain your choice", blank=True)

    p2_q5 = models.IntegerField(
        label='5. Suppose that you could choose to <b>bid</b> in an auction for one of the following two lottery tickets displayed above. Which one would you prefer?',
        choices=[
            [1, 'I prefer to bid for lottery A'],
            [2, 'I prefer to bid for lottery B'],
            [3, "I don't care"],
        ],
        widget=widgets.RadioSelect
    )
    p2_q5_explain = models.LongStringField(label="Explain your choice", blank=True)

    p3_q1 = models.FloatField(label="A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?")
    p3_q2 = models.FloatField(label="If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?")
    p3_q3 = models.FloatField(label="In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake? ")


page_sequence = [
    PartOne, PartTwo, PartThree
]
