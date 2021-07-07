import random
from exp.db import BidHistory, PlayerBidHistory


class ExperimentSubSession:
    def get_lottery_ids(self, num_lotteries, prefix):
        return [
            int(self.session.config[lottery_key])
            for lottery_key in [
                f"{prefix}{key}"
                for key in range(1, num_lotteries + 1)
            ]
        ]

    def get_treatment_code(self) -> str:
        treatment_code = self.session.config["treatment"].strip()
        assert treatment_code == "cp" or treatment_code == "cv"
        return treatment_code


def save_bid_history_to_player(player, rounds_per_lottery,  player_bid_history: PlayerBidHistory):
    player.rounds_per_lottery = rounds_per_lottery
    bid_history: BidHistory = player_bid_history.bid_history
    # Player Bid History
    player.player_bid_history_id = player_bid_history.id
    player.lottery_order = player_bid_history.lottery_order
    player.lottery_round_number = player_bid_history.lottery_round_number
    # Bid History
    player.bid_history_id = bid_history.id
    player.previous_session_id = bid_history.session_id
    player.lottery_id = bid_history.lottery_id
    player.treatment = bid_history.treatment_code
    player.part_round_number = bid_history.part_round_number
    player.others_group_id = bid_history.group_id
    player.others_player_id = bid_history.player_id
    player.alpha = bid_history.alpha
    player.beta = bid_history.beta
    player.epsilon = bid_history.epsilon
    player.ticket_value_before = bid_history.ticket_value_before
    player.ticket_probability = bid_history.ticket_probability
    player.fixed_value = bid_history.fixed_value
    player.ticket_value_after = bid_history.ticket_value_after
    player.be_bid = bid_history.be_bid
    player.signal = bid_history.signal4
    player.signal1 = bid_history.signal1
    player.signal2 = bid_history.signal2
    player.signal3 = bid_history.signal3
    player.signal4 = bid_history.signal4
    player.bid1 = bid_history.bid1
    player.bid2 = bid_history.bid2
    player.bid3 = bid_history.bid3
    player.bid4 = bid_history.bid4
    player.up_ticket = round(bid_history.up_ticket * 100)
    player.others_high_bid = bid_history.other_high_bid


def create_player_bid_histories(treatment_code, players, lottery_ids, session_id, rounds_per_lottery, phase):
    BidHistory.excel_to_db()
    PlayerBidHistory.create_db()

    for player in players:
        for index, lottery_id in enumerate(lottery_ids):
            for lottery_round_number in range(1, rounds_per_lottery + 1):
                unused_bid_histories = BidHistory.get_unused_bid_histories(
                    lottery_id,
                    treatment_code,
                    session_id,
                    player.participant.id,
                )
                print(f"Retrieved {len(unused_bid_histories)} out of {rounds_per_lottery} unused bid histories for participant {player.participant.id}.")

                # bid_history = unused_bid_histories[lottery_round_number - 1]
                bid_history = random.choice(unused_bid_histories)

                PlayerBidHistory.add_bid_history(
                    bid_history=bid_history,
                    session_id=session_id,
                    lottery_round_number=lottery_round_number,
                    participant_id=player.participant.id,
                    lottery_order=index + 1,
                    phase=phase
                )


def save_bid_history_for_all_players(players, rounds_per_lottery, phase):
    for player in players:
        player_bid_history: PlayerBidHistory = PlayerBidHistory.get_player_bid_history(
            session_id=player.subsession.session.id,
            lottery_round_number=player.get_lottery_round_number(rounds_per_lottery),
            lottery_order=player.get_lottery_order(rounds_per_lottery),
            participant_id=player.participant.id,
            phase=phase
        )
        save_bid_history_to_player(player, rounds_per_lottery, player_bid_history)


class BidHistoryPlayer:
    def is_part_one_payoff(self, rounds_per_lottery):
        lottery_number = self.get_lottery_order(rounds_per_lottery)
        round_number = self.get_lottery_round_number(rounds_per_lottery)
        payoff_round = self.participant.vars['part_one_payoff_round']
        payoff_lottery = self.participant.vars['part_one_payoff_lottery']
        return round_number == payoff_round and lottery_number == payoff_lottery

    def is_highest_bidder(self):
        return self.bid > self.bid1 and self.bid > self.bid2 and self.bid >= self.bid3

    def is_bid_tied(self):
        return self.bid == self.bid1 or self.bid == self.bid2 or self.bid == self.bid3

    def break_tie(self):
        return random.choice([True, False])

    def highest_bid(self):
        return max([self.bid, self.bid1, self.bid2, self.bid3])

    def previous_highest_bid(self):
        return max([self.bid1, self.bid2, self.bid3])

    @property
    def prep_worth(self):
        return self.up_ticket * self.fixed_value / 100

    @property
    def payoff_question_number(self):
        return self.participant.vars['question_phase_payoff_question_number']

    def get_bid_payoff_data(self):
        return self.participant.vars['bid_payoff_data']

    def get_bid_earnings(self):
        return self.participant.vars['bid_payoff_data']['earnings']

    def get_guess_earnings(self):
        return self.participant.vars['guess_payoff_data']['earnings']

    def get_lottery_round_number(self, rounds_per_lottery):
        # Calculates the relative round number given the oTree round number
        return (self.round_number - 1) % rounds_per_lottery + 1

    def get_lottery_order(self, rounds_per_lottery):
        # Calculates the lottery ID number given the oTree round number
        return ((self.round_number - 1) // rounds_per_lottery) + 1

    @property
    def lottery_number(self):
        return self.get_lottery_order()

    @property
    def is_probability_treatment(self):
        return self.session_treatment == "cp"

    @property
    def is_value_treatment(self):
        return self.session_treatment == "cv"

    @property
    def selected_value_text(self):
        return "Selected Value" if self.is_value_treatment else "Selected Probability"

    @property
    def value_text(self):
        return "value" if self.is_value_treatment else "probability"

    @property
    def selected_values_text(self):
        return "Selected Values" if self.is_value_treatment else "Selected Probabilities"


    @property
    def treatment_suffix(self):
        return "%" if self.is_probability_treatment else ""

    @property
    def session_treatment(self):
        return self.subsession.session.config["treatment"]

    @property
    def min_signal(self):
        return self.signal - self.epsilon

    @property
    def max_signal(self):
        return self.signal + self.epsilon

    @property
    def lottery_max_value(self):
        if self.is_probability_treatment:
            return self.fixed_value
        else:
            return self.beta
