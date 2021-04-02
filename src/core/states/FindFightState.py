from core.tools.FightFinder import find_fight_on_map
from core import env, dofus
from core.states.BaseState import BaseState
from core.tools.IsInFightCheck import is_in_fight

import time
import cv2


class FindFightState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)

    def on_enter(self):
        pass

    def update(self):
        if is_in_fight():
            self.change_state("Fight")
            return
        map_before_z = dofus.COMBAT_R.capture()
        env.press("z")
        time.sleep(0.3)
        map_after_z = dofus.COMBAT_R.capture()
        env.release("z")

        cv2.imwrite("/tmp/im1.png", map_before_z)
        cv2.imwrite("/tmp/im2.png", map_after_z)

        fight = find_fight_on_map(map_before_z, map_after_z)

        for f in fight:
            if f.lvl < 80:
                x, y, w, h = f.pixel_rect
                dofus.COMBAT_R.click(int(x + w/2), int(y + 3*h/4))
                time.sleep(2)
                env.move(0, 0)
                return
        print("no good fight found")
        time.sleep(1)

    def on_exit(self):
        pass


