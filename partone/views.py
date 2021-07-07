import random

import ibis
from pathlib import Path

from otree.api import Page, cu

from .constants import Constants


class Bid(Page):
    form_model = "player"
    form_fields = ["bid"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                )
        }

    @staticmethod
    def before_next_page(player, timeout_happened):

        if player.is_part_one_payoff(Constants.ROUNDS_PER_LOTTERY):
            player.is_payment_round = True

            if player.is_highest_bidder():
                player.new_highest_bid = player.bid
                player.tie = False
                player.winner = True
                player.earnings = player.ticket_value_after - player.bid
            elif player.is_bid_tied():
                player.new_highest_bid = player.bid
                player.tie = True
                player.win_tie_break = player.break_tie()
                if player.win_tie_break:
                    player.earnings = player.ticket_value_after - player.bid
                else:
                    player.earnings = 0
                player.winner = player.win_tie_break
            else:
                player.new_highest_bid = player.highest_bid()
                player.tie = False
                player.winner = False
                player.earnings = 0

            player.participant.vars['part_one_bid_payoff_data'] = {
                "bid": player.bid,
                "new_highest_bid": player.new_highest_bid,
                "tie": player.tie,
                "win_tie_break": player.win_tie_break,
                "winner": player.winner,
                "previous_highest_bid": player.previous_highest_bid(),
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "earnings": player.earnings,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability
            }
        else:
            player.is_payment_round = True


class Outcome(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.NUM_LOTTERIES * Constants.ROUNDS_PER_LOTTERY

    @staticmethod
    def vars_for_template(player):
        earnings = player.ticket_value_after - player.bid
        return {
            "player": player,
            **player.participant.vars['part_one_bid_payoff_data']
        }


class BestGuess(Page):
    form_model = "player"
    form_fields = ["guess"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_value": Constants.MIN_VALUATION,
            "max_value": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                ),
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
        )


class Interval(Page):
    form_model = "player"
    form_fields = ["guess", "min_guess", "max_guess"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                ),
            "signal": player.signal,
            "signal1": player.signal1,
            "signal2": player.signal2,
            "signal3": player.signal3,
            "signal4": player.signal4,
        }

    @staticmethod
    def error_message(player, values):
        if values["min_guess"] > values["guess"] or values["max_guess"] < values["guess"]:
            return f"Invalid values entered."



    @staticmethod
    def js_vars(player):
        return dict(
            display_intro=(player.round_number == 1),
            guess=player.guess,
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
        )


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.session_treatment}


