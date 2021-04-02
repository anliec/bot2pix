from core.states.BaseMachine import BaseMachine

from core.states.FightState import FightState
from core.states.WaitingForFight import WaitingForFightState
from core.states.FindFightState import FindFightState


class BotStateMachine(BaseMachine):
    def __init__(self):
        super().__init__()
        self.states["Fight"] = FightState(machine=self)
        # self.states["WaitingForFight"] = WaitingForFightState(machine=self)
        self.states["FindFight"] = FindFightState(machine=self)

        self.current_states = self.states["FindFight"]




