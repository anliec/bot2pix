

class BaseMachine:
    def __init__(self):
        self.states = {}
        self.current_states = None

    def change_state(self, new_state: str):
        print("StateMachine: Going to '{}'".format(new_state))
        self.current_states.on_exit()
        self.current_states = self.states[new_state]
        self.current_states.on_enter()

    def update(self):
        self.current_states.update()
