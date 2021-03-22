from core.states.BaseState import BaseState


class DisabledState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def update(self):
        pass


