from otree.api import Page


class PartOne(Page):
    form_model = 'player'
    form_fields = ['p1_q1', 'p1_q2', 'p1_q3']


class PartTwo(Page):
    form_model = 'player'
    form_fields = ['p2_q1', 'p2_q2', 'p2_q3a', 'p2_q3b', 'p2_q3c', 'p2_q3d',  'p2_q4', 'p2_q4_explain', 'p2_q5', 'p2_q5_explain']


class PartThree(Page):
    form_model = 'player'
    form_fields = ['p3_q1', 'p3_q2', 'p3_q3']
