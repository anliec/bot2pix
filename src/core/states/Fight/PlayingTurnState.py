from core.states.BaseState import BaseState
from core.states.Fight.WaitingForTurnState import READY_BUTTON_DISABLED, READY_BUTTON_ACTIVE
from core import env, dofus, Map
from core.tools.CombatMapParser import CombatMapParser
from core.tools.MapManager import is_tile_visible, find_shortest_path
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
        end_turn_button = dofus.READY_R.capture()
        if (end_turn_button == READY_BUTTON_DISABLED).any():
            self.change_state("WaitingForTurn")
            return
        elif not ((end_turn_button == READY_BUTTON_ACTIVE).any() or (end_turn_button == READY_BUTTON_DISABLED).any()):
            # It look like the fight ended as the ready / end turn button is not here anymore
            self.change_state("FightEnd")
            return
        map_obj, player_info = self.map_parser.parse_map(is_placement_stage=False)
        pa = read_pa()
        pm = read_pm()
        # TODO manage the case where there is more than one player in my team
        my_pos = player_info["red"][0]
        blue = sorted([(b, map_obj.dist(b, my_pos)) for b in player_info["blue"]], key=lambda x: x[1])
        for b_pos, b_dist in blue:
            is_visible = is_tile_visible(map_obj, my_pos, b)
            for attack in Player().attacks:
                if attack.pa_cost > pa:
                    continue
                if attack.need_visibility and not is_visible:
                    continue
                if attack.min_range <= b_dist <= attack.max_range:
                    # look like we can attack!
                    for key in attack.key_shortcut:
                        env.press(key)
                    time.sleep(0.1)
                    self.map_parser.click_on_tile(b_pos)
                    time.sleep(0.1)
                    for key in attack.key_shortcut:
                        env.release(key)
                    time.sleep(0.5)
                    # we have done one action return and wait the next update
                    return
        # Look like we can't attack anyone right now, try to move
        if pm > 0 and pa > 3:
            # if we still have pa and pm let's move to see if we can attack more
            path = find_shortest_path(map_obj, my_pos, blue[0][0])
            self.map_parser.click_on_tile(path[pm])
            time.sleep(0.5)
            return
        # we have no pa or pm left let's just end the turn
        dofus.READY_R.click()
        time.sleep(0.5)
        return

