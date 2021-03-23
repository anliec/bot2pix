from core.states.BaseMachine import BaseMachine

from core.states.Fight.DisabledState import DisabledState
from core.states.Fight.FightEndState import FightEndState
from core.states.Fight.PositionSelectionState import PositionSelectionState
from core.states.Fight.PlayingTurnState import PlayingTurnState
from core.states.Fight.WaitingForTurnState import WaitingForTurnState


class FightMachine(BaseMachine):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.states["Disabled"] = DisabledState(machine=self)
        self.states["FightEnd"] = FightEndState(machine=self)
        self.states["PositionSelection"] = PositionSelectionState(machine=self)
        self.states["PlayingTurn"] = PlayingTurnState(machine=self)
        self.states["WaitingForTurn"] = WaitingForTurnState(machine=self)

        self.current_states = self.states["Disabled"]

    def on_combat_ended(self):
        self.controller.on_combat_ended()



