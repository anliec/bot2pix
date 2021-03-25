from core.states.BaseState import BaseState
from core import env, dofus, Map
from core.tools.CombatMapParser import CombatMapParser
from core.tools.MapManager import is_tile_visible, find_shortest_path
from core.tools.CombatManager import is_ready_button_disabled, is_ready_button_visible, is_ready_button_enabled
from core.ScaleManager import ScaleManager
from core.tools.CombatStatsParser import read_pa, read_pm
from core.player.Player import Player

import numpy as np
import time


class PlayingTurnState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)
        self.map_parser = CombatMapParser()

    def update(self):
        # first check that it's still our turn
        if is_ready_button_disabled():
            print("Time probably run out, our turn is finished")
            self.change_state("WaitingForTurn")
            return
        elif not is_ready_button_visible():
            # It look like the fight ended as the ready / end turn button is not here anymore
            print("Fight ended, victory?")
            self.change_state("FightEnd")
            return
        map_obj, player_info = self.map_parser.parse_map(is_placement_stage=False)
        pa = read_pa()
        pm = read_pm()
        # TODO manage the case where there is more than one player in my team
        if len(player_info["red"]) == 0:
            # Well let's hope it's not too bad, wait and see
            time.sleep(1.0)
            return
        my_pos = player_info["red"][0]
        blue = sorted([(b, map_obj.dist(b, my_pos)) for b in player_info["blue"]], key=lambda x: x[1])
        for b_pos, b_dist in blue:
            is_visible = is_tile_visible(map_obj, my_pos, b_pos)
            for attack in Player().attacks:
                if attack.pa_cost > pa:
                    print('not enough pa for {}'.format(attack.name))
                    continue
                if attack.need_visibility and not is_visible:
                    print('no visibility for {}'.format(attack.name))
                    continue
                if attack.min_range <= b_dist <= attack.max_range:
                    print("Launching attack {}".format(attack.name))
                    print("  my pos: {}".format(my_pos))
                    print("  target pos: {}".format(b_pos))
                    print("  dist: {}".format(b_dist))
                    # look like we can attack!
                    for key in attack.key_shortcut:
                        env.press(key)
                    time.sleep(0.1)
                    for key in attack.key_shortcut:
                        env.release(key)
                    time.sleep(0.1)
                    self.map_parser.click_on_tile(b_pos)
                    time.sleep(0.1)
                    # reset cursor to make sure the ready button is visible
                    dofus.READY_R.hover()
                    # long wait here to let the to a dead boone to disappear
                    # and for the damage to disappear
                    # ultimately this can be avoided if we don't parse the whole map every action, or by smarter
                    # image recognition methods
                    time.sleep(4.0)
                    # we have done one action return and wait the next update
                    return
                else:
                    print('no range for {} (dist: {})'.format(attack.name, b_dist))
        # Look like we can't attack anyone right now, try to move
        if pm > 0 and len(blue) > 0:
            # if we still have pa and pm let's move to see if we can attack more
            path = find_shortest_path(map_obj, np.array(my_pos), np.array(blue[0][0]))
            move_pos = None
            if len(path) > pm + 1:
                move_pos = path[pm - 1]
            elif len(path) > 1:
                move_pos = path[-2]
            if move_pos is not None:
                self.map_parser.click_on_tile(move_pos)
                dofus.READY_R.hover()
                time.sleep(1)
                return
            # if the path is empty, we can continue and end the turn
        elif len(blue) == 0:
            print("No blue team member seen on the map !!!")
        # we have no pa or pm left let's just end the turn
        time.sleep(0.5)
        # try to avoid clicking on this button at the end of the fight
        if is_ready_button_enabled():
            dofus.READY_R.click()
        return

