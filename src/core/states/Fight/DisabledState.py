from core.states.BaseState import BaseState

import time


class DisabledState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        time.sleep(0.1)


