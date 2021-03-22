from core.states.BaseState import BaseState
from core import env, dofus, Map
from core.tools.CombatMapParser import CombatMapParser
from core.ScaleManager import ScaleManager

import numpy as np
import time

# TODO: get this info from player's attack directly
PREFERED_MAX_DIST = 6
PREFERED_MIN_DIST = 1

IS_BOONE_MODE_COLOR = np.array((1, 250, 218))


class PositionSelectionState(BaseState):
    def __init__(self, machine):
        super().__init__(machine)
        self.map_parser = CombatMapParser()

    def update(self):
        is_boone_img = dofus.CREATURE_MODE_R.capture()
        if not (is_boone_img == IS_BOONE_MODE_COLOR).any():
            # We are not in boone mode, fix that and wait a bit to apply
            dofus.CREATURE_MODE_R.click()
            time.sleep(1)
        map_obj, player_info = self.map_parser.parse_map(is_placement_stage=True)
        starting_pos = self.get_best_starting_pos(map_obj, player_info)
        if map_obj.is_tile_walkable(starting_pos):
            self.map_parser.click_on_tile(starting_pos)
        else:
            # Lets assume that it's because we are already there for now...
            dofus.READY_R.click()
            time.sleep(1)
            self.machine.change_state("WaitingForTurn")

    def get_best_starting_pos(self, map_obj:Map.Map, player_info):
        blue_players = player_info["blue"]
        red_possible_pos = player_info["red_start_pos"]
        best_score = -1
        best_pos = None
        # TODO: take into account that some tile are occupied (need to know where we are...)
        for possible_pos in red_possible_pos:
            score = 0
            for blue_player in blue_players:
                d = map_obj.dist(possible_pos, blue_player)
                if PREFERED_MIN_DIST <= d <= PREFERED_MAX_DIST:
                    score += 10
                elif d < PREFERED_MIN_DIST:
                    score += max(0, 10 - PREFERED_MIN_DIST + d)
                elif d > PREFERED_MAX_DIST:
                    score += max(0, 10 - d + PREFERED_MAX_DIST)
            if score > best_score:
                best_score = score
                best_pos = possible_pos
        return best_pos
