from core.states.BaseState import BaseState
from core import env

import time


class FightEndState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        # close UI
        print("Fight ended")
        env.press("enter")
        time.sleep(0.1)
        env.release("enter")
        time.sleep(1)
        self.machine.on_combat_ended()


