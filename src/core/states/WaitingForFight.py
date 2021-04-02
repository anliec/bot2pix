from core.states.BaseState import BaseState
from core.tools.IsInFightCheck import is_in_fight

import time


class WaitingForFightState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        if is_in_fight():
            self.change_state("Fight")
        else:
            # let's not loop too quickly
            time.sleep(0.5)





