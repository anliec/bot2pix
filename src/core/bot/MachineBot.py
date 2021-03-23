from core.states.BotStateMachine import BotStateMachine
from core import env
from core.player.Player import Player
from core.player.Attack import Attack


class MachineBot:
    def __init__(self, character_name):
        self.character_name = character_name
        env.focusDofusWindow(character_name)
        # capture the whole screen to initialise scale manager
        env.capture(None)
        self.machine = BotStateMachine()

    def run(self):
        while True:
            self.machine.update()


def main():
    attaque_naturelle = Attack()
    attaque_naturelle.name = "Attaque Naturelle"
    attaque_naturelle.pa_cost = 3
    attaque_naturelle.max_range = 7
    attaque_naturelle.min_range = 1
    attaque_naturelle.need_visibility = True
    attaque_naturelle.key_shortcut = ['2']
    Player().attacks = [attaque_naturelle]
    bot = MachineBot("Pif-Protect")

    bot.run()

    
if __name__ == '__main__':
    main()

