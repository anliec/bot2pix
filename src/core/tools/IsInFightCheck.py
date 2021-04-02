from core import env, dofus
from core.tools.CombatManager import is_ready_button_enabled

import numpy as np

COUNT_DOWN_TIMER_COLOR = np.array((0, 200, 252))
READY_BUTTON_ACTIVE = np.array((0, 240, 206))


def is_in_fight():
    my_turn_check_im = dofus.MY_TURN_CHECK_R.capture()
    if (my_turn_check_im == COUNT_DOWN_TIMER_COLOR).any():
        # case one: the progress bar is yellow
        return True
    elif is_ready_button_enabled():
        # case two: the ready / skip turn button is in the UI
        return True
    return False


