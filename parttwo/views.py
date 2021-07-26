import random

import ibis
from pathlib import Path

from otree.api import Page, cu

from .constants import Constants

class Choice(Page):
    form_model = "player"
    form_fields = ["strategy_choice"]

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


class Outcome(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.session_treatment}


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
                ),
            "guess": player.get_guess(),
            "min_guess": player.get_min_guess(),
            "max_guess": player.get_max_guess(),
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            highest_signal=loader('HighestSignal.html').render({"player": player}),
            belief=loader('Belief.html').render({"player": player}),
            right_top_ticket_info=loader('RightTopTicketInfo.html').render({"player": player}),
            right_bottom_ticket_info=loader('RightBottomTicketInfo.html').render({"player": player}),
            your_bid_one=loader('YourBidPartOne.html').render({"player": player}),
            your_bid_two=loader('YourBidPartTwo.html').render({"player": player}),
            your_guess=loader('YourGuess.html').render({"player": player}),
            right_lottery_info=loader('RightLotteryInfo.html').render({"player": player}),
            lottery_expected_payoff=loader('LotteryExpectedPayoffInfo.html').render({"player": player}),
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
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

        if player.is_part_one_payoff(Constants.ROUNDS_PER_LOTTERY):
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


class BidInfo(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                ),
            "guess": player.get_guess(),
            "min_guess": player.get_min_guess(),
            "max_guess": player.get_max_guess(),
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            lottery_ticket_signal=loader('LotteryTicketSignalInfo.html').render({"player": player}),
            highest_signal=loader('HighestSignal.html').render({"player": player}),
        )
