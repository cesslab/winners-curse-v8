from otree.api import *

from exp.models import (
    BidHistoryPlayer,
)

c = Currency

doc = """
Payoff
"""


class Constants(BaseConstants):
    name_in_url = 'payoff'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    final_payoff_dollars = models.CurrencyField()


# PAGES
class BidPayoff(Page):
    @staticmethod
    def vars_for_template(player):
        return player.participant.vars['bid_payoff_data']


class PayoffDebug(Page):
    @staticmethod
    def vars_for_template(player):
        return {
              **player.participant.vars['bid_payoff_data'],
              **player.participant.vars['guess_payoff_data']
        }


class GuessPayoff(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "selected_value_text": player.selected_value_text,
            **player.participant.vars['guess_payoff_data']
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        bid_earnings_credits = player.get_bid_earnings()
        guess_earnings_credits = player.get_guess_earnings()

        player.payoff = 10.0 + 12.0 + (bid_earnings_credits/6.0) + (guess_earnings_credits/6.0)
        print(f"saving final payoff of {player.payoff}")


class FinalPayoff(Page):
    @staticmethod
    def vars_for_template(player: Player):
        bid_earnings_credits = player.get_bid_earnings()
        guess_earnings_credits = player.get_guess_earnings()

        bid_earnings_dollars = cu(round(bid_earnings_credits/6.0, 2)).to_real_world_currency(player.session)
        guess_earnings_dollars = cu(round(guess_earnings_credits/6.0, 2)).to_real_world_currency(player.session)
        return {
            "bid_earnings_credits": bid_earnings_credits,
            "bid_earnings_dollars": bid_earnings_dollars,
            "guess_earnings_credits": guess_earnings_credits,
            "guess_earnings_dollars": guess_earnings_dollars,
            "final_payment": player.payoff
        }


class QuestionPayoffDebug(Page):
    @staticmethod
    def vars_for_template(player):
        part_one_payoff_data = player.participant.vars['bid_payoff_data']
        if player.payoff_question_number == 1:
            part_two_payoff_data = player.question_one_data
        elif player.payoff_question_number == 2:
            part_two_payoff_data = player.question_three_data
        else:
            part_two_payoff_data = player.question_two_data

        return {
            "selected_value_text": player.selected_value_text,
            **part_one_payoff_data,
            **part_two_payoff_data,
            "question_number": player.payoff_question_number,
        }


page_sequence = [GuessPayoff, BidPayoff, FinalPayoff, PayoffDebug]
