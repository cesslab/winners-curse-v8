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

            player.participant.vars['bid_payoff_data'] = {
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
    def before_next_page(player, timeout_happened):

        if player.is_part_one_payoff(Constants.ROUNDS_PER_LOTTERY):
            #  Emin = fix * alpha
            #  Emax = fix * beta
            player.prep_emin = player.fixed_value * player.alpha / 100
            player.prep_emax = player.fixed_value * player.beta / 100

            # ---------------------------------------------------------------------
            # Question 1a: point belief about highest of the other 3 bids
            # ---------------------------------------------------------------------
            # Computer computes loss function L= (X-OthersHBid)^2
            player.computed_loss = float((player.guess - player.others_high_bid) ** 2)
            # Computer draws random number K ~ U[0,1296]
            MAX_DISTANCE = 1296
            player.random_k = random.randint(0, MAX_DISTANCE)
            # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296)
            # (Note: For the upper threshold of K we took the maximum distance (Emax-Emin) ^ 2 = 36 ^ 2.)
            player.l_less_than_k = player.computed_loss < player.random_k
            if player.l_less_than_k:
                player.guess_earnings = 12.0
            else:
                player.guess_earnings = 0.0

            player.prob_k_greater_than_l = int(((MAX_DISTANCE - player.computed_loss) / MAX_DISTANCE) * 100.0)
            # ---------------------------------------------------------------------
            # Question 1b: confidence interval about worth of the lottery.
            # ---------------------------------------------------------------------
            # Computer computes 12*[1- (u-l)/(Emax-Emin)] if positive and OthersHBid in [l,u] (worth is in interval); 0 otherwise
            player.confidence_value = round(12.0 * (
                1.0 - (float(player.max_guess - player.min_guess) / float(player.prep_emax - player.prep_emin))),
                                            2)
            player.high_bid_within_interval = player.min_guess <= player.others_high_bid <= player.max_guess
            player.computed_value_non_zero = player.confidence_value > 0.0
            if player.computed_value_non_zero and player.high_bid_within_interval:
                player.interval_earnings = player.confidence_value
            else:
                player.interval_earnings = 0

            player.is_payment_round = True
            player.participant.vars['guess_payoff_data'] = {
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability,
                "is_probability_treatment": player.is_probability_treatment,
                "is_value_treatment": player.is_value_treatment,
                # Question 1 Variables
                # "prob": player.prob_k_greater_than_l,
                "prob_k_greater_than_l": player.prob_k_greater_than_l,
                "prep_emax": player.prep_emax,
                "prep_emin": player.prep_emin,
                "guess_earnings": player.guess_earnings,
                "max_guess": player.max_guess,
                "min_guess": player.min_guess,
                "guess": player.guess,
                "interval_earnings": player.interval_earnings,
                "earnings": player.guess_earnings + player.interval_earnings,
                # "is_worth_within_interval": player.is_others_high_bid_within_interval,
                "high_bid_within_interval": player.high_bid_within_interval,
                "prep_worth": player.prep_worth,
                "random_k": player.random_k,
                "computed_loss": player.computed_loss,
                "confidence_value": player.confidence_value,
                # "is_guess_sufficiently_close_to_worth": player.l_less_than_k,
                "l_less_than_k": player.l_less_than_k,
                "computed_value_non_zero": player.computed_value_non_zero,
                "others_high_bid": player.others_high_bid,
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


