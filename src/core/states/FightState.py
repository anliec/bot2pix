from core.states.BaseState import BaseState

from core.states.Fight.CombatStateMachine import FightMachine


class FightState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)
        self.sub_state_machine = FightMachine(controller=self)

    def on_enter(self):
        self.sub_state_machine.change_state("PositionSelection")

    def update(self):
        self.sub_state_machine.update()

    def on_exit(self):
        self.sub_state_machine.change_state("Disabled")

    def on_combat_ended(self):
        self.change_state("FindFight")



