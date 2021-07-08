from otree.api import *

from exp.models import BidHistoryPlayer

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    q1 = models.IntegerField(
        label='1. Suppose that you are not the highest bidder in an auction. How much do you have to pay?',
        choices=[[1, 'Your bid'], [2, 'The highest bid'], [3, 'Nothing']],
        widget=widgets.RadioSelect
    )
    cp_q2 = models.IntegerField(
        label='2. Which of the following alternatives is correct?',
        choices=[
            [1, 'All four bidders bid for the same lottery ticket with the same Selected Probability.'],
            [2, 'All four bidders bid for lottery tickets with different Selected Probabilities.'],
            [3, 'All four bidders bid for lottery tickets with possibly different Selected Probabilities.']],
        widget=widgets.RadioSelect
    )
    cv_q2 = models.IntegerField(
        label='2. Which of the following alternatives is correct?',
        choices=[
            [1, 'All four bidders bid for the same lottery ticket with the same Selected Value.'],
            [2, 'All four bidders bid for lottery tickets with different Selected Value.'],
            [3, 'All four bidders bid for lottery tickets with possibly different Selected Value.']],
        widget=widgets.RadioSelect
    )
    cp_q3 = models.IntegerField(
        label='3. Which of the following alternatives is correct?',
        choices=[
            [1, 'All four bidders receive the same signal about the same Selected Probability.'],
            [2, 'All four bidders receive possibly different signals about the same Selected Probability.'],
            [3, 'All four bidders receive different signals because Selected Probabilities differ for each of them.']],
        widget=widgets.RadioSelect
    )
    cv_q3 = models.IntegerField(
        label='3. Which of the following alternatives is correct?',
        choices=[
            [1, 'All four bidders receive the same signal about the same Selected Value.'],
            [2, 'All four bidders receive possibly different signals about the same Selected Value.'],
            [3, 'All four bidders receive different signals because Selected Value differ for each of them.']],
        widget=widgets.RadioSelect
    )
    cp_q4 = models.IntegerField(
        label='4. Suppose you win the lottery ticket in a given auction. What are your earnings from this auction?',
        choices=[
            [1, 'The non-zero value of the lottery minus your bid.'],
            [2, 'The outcome of the lottery minus your bid.']],
        widget=widgets.RadioSelect
    )
    cv_q4 = models.IntegerField(
        label='4. Suppose you win the lottery ticket in a given auction. What are your earnings from this auction?',
        choices=[
            [1, 'The Selected Value of the lottery minus your bid.'],
            [2, 'The outcome of the lottery minus your bid.']],
        widget=widgets.RadioSelect
    )
    cp_q5 = models.IntegerField(
        label='5. Suppose that you receive a signal 30 that is at most 4 percentage points away from the Selected Probability. What could be the Selected Probability?',
        choices=[
            [1, '18%'],
            [2, '28%'],
            [3, '38%']],
        widget=widgets.RadioSelect
    )
    cv_q5 = models.IntegerField(
        label='5. Suppose that you receive a signal of 30 that is at most 4 units away from the Selected Value. What could be the Selected Value?',
        choices=[
            [1, '18'],
            [2, '28'],
            [3, '38']],
        widget=widgets.RadioSelect
    )
    cp_q6 = models.IntegerField(
        label='6. Suppose the Selected Probability is 30%. The outcome of the lottery in credits...',
        choices=[
            [1, 'can only be 70'],
            [2, '21 ( = 30% x 70 + 70% x 0)'],
            [3, 'can be 0 or 70']],
        widget=widgets.RadioSelect
    )
    cv_q6 = models.IntegerField(
        label='6. Suppose the Selected Value is 30.The outcome of the lottery in credits...',
        choices=[
            [1, 'can only be 30'],
            [2, '21 ( = 30 x 70% +  0 x 30%)'],
            [3, 'can be 0 or 30']],
        widget=widgets.RadioSelect
    )
    signal = models.IntegerField(initial=30)
    alpha = models.IntegerField(initial=20)
    beta = models.IntegerField(initial=40)
    epsilon = models.IntegerField(initial=4)
    ticket_value_before = models.IntegerField(initial=0)
    ticket_probability = models.IntegerField(initial=70)
    fixed_value = models.IntegerField(initial=70)
    ticket_value_after = models.IntegerField(initial=0)


# PAGES
class Quiz(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.is_value_treatment:
            return ['q1', 'cv_q2', 'cv_q3', 'cv_q4', 'cv_q5', 'cv_q6']
        else:
            return ['q1', 'cp_q2', 'cp_q3', 'cp_q4', 'cp_q5', 'cp_q6']

Error_Message = 'Incorrect answer. If you do not understand why your answer is wrong, please send a private message to the experimenter.'

def q1_error_message(player: Player, value):
    if value != 3:
        return Error_Message


def cv_q2_error_message(player: Player, value):
    if value != 1:
        return  Error_Message


def cp_q2_error_message(player: Player, value):
    if value != 1:
        return Error_Message

def cv_q3_error_message(player: Player, value):
    if value != 2:
        return Error_Message


def cp_q3_error_message(player: Player, value):
    if value != 2:
        return Error_Message


def cv_q4_error_message(player: Player, value):
    if value != 2:
        return Error_Message


def cp_q4_error_message(player: Player, value):
    if value != 2:
        return Error_Message


def cv_q5_error_message(player: Player, value):
    if value != 2:
        return Error_Message


def cp_q5_error_message(player: Player, value):
    if value != 2:
        return Error_Message


def cv_q6_error_message(player: Player, value):
    if value != 3:
        return Error_Message


def cp_q6_error_message(player: Player, value):
    if value != 3:
        return Error_Message


page_sequence = [Quiz]
