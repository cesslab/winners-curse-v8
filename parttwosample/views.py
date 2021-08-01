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


class BidSample(Page):
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
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            # Benchmarks
            guess=player.get_guess(),
            min_guess=player.get_min_guess(),
            max_guess=player.get_max_guess(),
            one_minus_p=(100-player.fixed_value) if player.is_value_treatment else (100-player.up_ticket),
            exp_payoff=player.prep_worth,
            exp_value=player.up_ticket if player.is_value_treatment else player.fixed_value,
            exp_value_prob=player.fixed_value if player.is_value_treatment else player.up_ticket,
            is_value_treatment=player.is_value_treatment,
            display_intro=(player.round_number == 1),
            # Walk-Through
            part_one_lottery_info=loader('PartOneLotteryInfo.html').render({"player": player}),
            highest_signal_info=loader('HighestSignalInfo.html').render({"player": player}),
            your_bid_one=loader('YourBidPartOne.html').render({"player": player}),
            your_bid_two=loader('YourBidPartTwo.html').render({"player": player}),
            benchmark_info=loader('BenchmarkInfo.html').render({"player": player}),
            benchmark_guess_info=loader('BenchmarkGuessInfo.html').render({"player": player}),
            benchmark_expected_lottery_info=loader('BenchmarkExpectedLotteryInfo.html').render({"player": player}),
            benchmark_expected_selected_value_info=loader('BenchmarkExpectedSelectedValueInfo.html').render({"player": player}),
            benchmark_expected_payoff_info=loader('BenchmarkExpectedPayoffInfo.html').render({"player": player}),
            benchmark_expected_lottery_continued_info=loader('BenchmarkExpectedLotteryContinuedInfo.html').render({"player": player}),
            # belief=loader('Belief.html').render({"player": player}),
            # right_top_ticket_info=loader('RightTopTicketInfo.html').render({"player": player}),
            # right_bottom_ticket_info=loader('RightBottomTicketInfo.html').render({"player": player}),
            # your_guess=loader('YourGuess.html').render({"player": player}),
            # right_lottery_info=loader('RightLotteryInfo.html').render({"player": player}),
            # lottery_expected_payoff=loader('LotteryExpectedPayoffInfo.html').render({"player": player}),
        )
