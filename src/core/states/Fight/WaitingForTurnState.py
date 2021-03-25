from core.states.BaseState import BaseState
from core.tools.CombatManager import is_ready_button_visible, is_ready_button_enabled
from core import dofus

import numpy as np
import time

COUNT_DOWN_TIMER_COLOR = np.array((0, 200, 252))


class WaitingForTurnState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        my_turn_check_im = dofus.MY_TURN_CHECK_R.capture()
        if (my_turn_check_im == COUNT_DOWN_TIMER_COLOR).any():
            print("Timer is visible, time to fight!")
            self.change_state("PlayingTurn")
        elif is_ready_button_enabled():
            print("Button enabled, time to fight!")
            self.change_state("PlayingTurn")
        elif not is_ready_button_visible():
            self.change_state("FightEnd")
        else:
            dofus.MY_TURN_CHECK_R.hover()
            time.sleep(0.5)




