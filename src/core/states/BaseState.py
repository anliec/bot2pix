

class BaseState:
    def __init__(self, machine):
        self.machine = machine

    def on_enter(self):
        pass

    def update(self):
        pass

    def on_exit(self):
        pass

    def change_state(self, state: str):
        self.machine.change_state(state)
