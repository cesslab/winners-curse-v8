import base64
import json
import hashlib
from otree.api import *

from exp.models import (
    BidHistoryPlayer,
)

doc = """
Venmo Payment
"""


class Constants(BaseConstants):
    name_in_url = 'venmo'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    confirmation_code = models.StringField(max_length=5)


# PAGES
class VenmoPayment(Page):
    form_model = "player"
    form_fields = ["confirmation_code"]

    @staticmethod
    def vars_for_template(player):
        session_id = player.subsession.session.id
        participant_id = player.participant.id
        float_payoff = float(player.participant.payoff_plus_participation_fee())
        payoff = player.participant.payoff_plus_participation_fee()
        data = {"esid": session_id, "pid": participant_id, "po": float_payoff}
        hasher = hashlib.sha256()
        hasher.update(json.dumps(data).encode())
        confirmation_code = hasher.hexdigest()[0:5]
        data["cc"] = confirmation_code
        data_json_byte_string = json.dumps(data).encode()
        print(data["cc"])

        encoded_data = base64.urlsafe_b64encode(data_json_byte_string).decode()
        return {
            "sid": session_id,
            "pid": participant_id,
            "po": float_payoff,
            "encoded_data": encoded_data,
            "payoff": payoff
        }

    @staticmethod
    def error_message(player, values):
        session_id = player.subsession.session.id
        participant_id = player.participant.id
        float_payoff = float(player.participant.payoff_plus_participation_fee())
        data = {"esid": session_id, "pid": participant_id, "po": float_payoff}
        hasher = hashlib.sha256()
        hasher.update(json.dumps(data).encode())
        confirmation_code = hasher.hexdigest()[0:5]
        print(confirmation_code)

        if values["confirmation_code"] != confirmation_code:
            return f"Your confirmation code is invalid."


class ExperimentComplete(Page):
    pass


page_sequence = [VenmoPayment, ExperimentComplete]
