from core.states.BaseState import BaseState
from core import dofus

import numpy as np

COUNT_DOWN_TIMER_COLOR = np.array((0, 200, 252))
READY_BUTTON_ACTIVE = np.array((0, 240, 206))
READY_BUTTON_DISABLED = np.array((0, 143, 124))


class WaintingForTurnState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        my_turn_check_im = dofus.MY_TURN_CHECK_R.capture()
        if (my_turn_check_im == COUNT_DOWN_TIMER_COLOR).any():
            self.change_state("PlayingTurn")

        end_turn_button = dofus.READY_R.capture()
        if not ((end_turn_button == READY_BUTTON_ACTIVE).any() or (end_turn_button == READY_BUTTON_DISABLED).any()):
            # It look like the fight ended as the ready / end turn button is not here anymore
            self.change_state("FightEnd")




