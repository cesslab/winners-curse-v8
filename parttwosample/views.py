import ibis
from pathlib import Path

from otree.api import Page, cu

from .constants import Constants


class Outcome(Page):
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
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
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
        loader = ibis.loaders.FileLoader(Path(__file__).parent.parent / 'parttwo')
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


class BidOne(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
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
        loader = ibis.loaders.FileLoader(Path(__file__).parent.parent / 'parttwo')
        return dict(
            display_intro=(player.round_number == 1),
            lottery_ticket_signal=loader('LotteryTicketSignalInfo.html').render({"player": player}),
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
