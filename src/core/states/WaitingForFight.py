from core.states.BaseState import BaseState
from core.tools.CombatManager import is_ready_button_enabled
from core import dofus

import numpy as np
import time

COUNT_DOWN_TIMER_COLOR = np.array((0, 200, 252))
READY_BUTTON_ACTIVE = np.array((0, 240, 206))


class WaitingForFightState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        my_turn_check_im = dofus.MY_TURN_CHECK_R.capture()
        if (my_turn_check_im == COUNT_DOWN_TIMER_COLOR).any():
            # case one: the progress bar is yellow
            self.change_state("Fight")
        elif is_ready_button_enabled():
            # case two: the ready / skip turn button is in the UI
            self.change_state("Fight")
        else:
            # let's not loop too quickly
            time.sleep(0.5)





