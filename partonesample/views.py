import random

import ibis
from pathlib import Path

from otree.api import Page, cu

from .constants import Constants


class Bid(Page):
    form_model = "player"

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
                )
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            alpha=player.alpha,
            beta=player.beta,
            epsilon=player.epsilon,
            signal=player.signal,
            min_signal=player.min_signal,
            max_signal=player.max_signal,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            your_task=loader('YourTask.html').render({"player": player}),
            bid_description_one=loader('BidDescriptionOne.html').render({"player": player}),
            bid_description_two=loader('BidDescriptionTwo.html').render({"player": player}),
            bid_description_three=loader('BidDescriptionThree.html').render({"player": player}),
            your_bid_one=loader('YourBidOne.html').render({"player": player}),
            your_bid_two=loader('YourBidTwo.html').render({"player": player}),
            lottery_types=loader('LotteryTypesIntro.html').render({"player": player}),
        )


class BestGuessLeft(Page):
    form_model = "player"

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
            lottery_ticket=loader('LotteryTicketIntro.html').render({"player": player}),
            your_signal=loader('YourSignalIntro.html').render({"player": player}),
            signal_interpretation=loader('SignalInterpretationIntro.html').render({"player": player}),
            question=loader('Question.html').render({"player": player}),
            instructions_for_slider=loader('InstructionsForSliderIntro.html').render({"player": player}),
            general_remark=loader('GeneralRemarkIntro.html').render({"player": player}),
            guess_task=loader('GuessTask.html').render({"player": player}),
        )

class BestGuessRight(Page):
    form_model = "player"

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
            lottery_ticket=loader('LotteryTicketIntro.html').render({"player": player}),
            your_signal=loader('YourSignalIntro.html').render({"player": player}),
            signal_interpretation=loader('SignalInterpretationIntro.html').render({"player": player}),
            question=loader('Question.html').render({"player": player}),
            instructions_for_slider=loader('InstructionsForSliderIntro.html').render({"player": player}),
            general_remark=loader('GeneralRemarkIntro.html').render({"player": player}),
            guess_task=loader('GuessTask.html').render({"player": player}),
            lottery_types=loader('LotteryTypesIntro.html').render({"player": player}),
        )

class Interval(Page):
    form_model = "player"

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
        }

    @staticmethod
    def error_message(player, values):
        if values["min_guess"] > values["guess"] or values["max_guess"] < values["guess"]:
            return f"Invalid values entered."

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            guess="",
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            interval_part_one=loader('IntervalPartOne.html').render({"player": player}),
            interval_part_two=loader('IntervalPartTwo.html').render({"player": player}),
            interval_limits=loader('IntervalLimits.html').render({"player": player}),
        )


class Outcome(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


class Payoff(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


class Summary(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


class InstructionsPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

