from otree.api import Page


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        treatment = player.subsession.get_treatment_code()
        return {"treatment": treatment}
