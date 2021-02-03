import os
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from core import Region, Location
from core.ScaleComputer import ScaleComputer

core_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
patterns_dir = os.path.join(core_path, "patterns")


def loadPattern(name):
    return cv2.imread(os.path.join(patterns_dir, name))


_default_scale = ScaleComputer(win_width=1920, win_height=1031, top_bar_decoration_offset=30)

RESIGN_POPUP_R = Region(698, 442, 533, 173, _default_scale)
DEFEAT_POPUP_R = Region(762, 696, 415, 141, _default_scale)
COMBAT_R = Region(335, 29, 1253, 885, _default_scale)
MINIMAP_R = Region(62, 876, 190, 122, _default_scale)
PM_R = Region(793, 993, 27, 34, _default_scale)
PA_R = Region(729, 983, 55, 42, _default_scale)
COMBAT_ENDED_POPUP_R = Region(841, 701, 244, 66, _default_scale)
READY_R = Region(1312, 925, 145, 66, _default_scale)
COMBAT_ENDED_POPUP_CLOSE_R = Region(1231, 721, 22, 18, _default_scale)
MY_TURN_CHECK_R = Region(841, 1009, 17, 8, _default_scale)
OUT_OF_COMBAT_R = Region(104, 749, 37, 37, _default_scale)
CREATURE_MODE_R = Region(1339, 993, 27, 25, _default_scale)
MAP_COORDS_R = Region(0, 28, 298, 98, _default_scale, absolute_coordinate=True)
CONNECT_R = Region(666, 88, 572, 531, _default_scale)
RECONNECT_BUTTON_R = Region(880, 381, 161, 57, _default_scale)
PLAY_GAME_BUTTON_R = Region(993, 652, 452, 260, _default_scale)
BANK_MAN_R = Region(935, 465, 121, 126, _default_scale)
BANK_MAN_TALK_R = Region(465, 601, 999, 236, _default_scale)
INV_OPEN_R = Region(1213, 76, 413, 138, _default_scale)
INV_FIRST_SLOT_R = Region(1249, 202, 67, 67, _default_scale)
LVL_UP_INFO_R = Region(0, 438, 486, 388, _default_scale)
SLOTS_R = Region(835, 920, 418, 86, _default_scale)
HAVRE_SAC_ZAAP_R = Region(525, 380, 79, 54, _default_scale)
ZAAP_CHOICES_R = Region(641, 268, 552, 461, _default_scale)
CHAT_R = Region(352, 972, 320, 31, _default_scale)
ZAAP_COORD_R = Region(1034, 295, 83, 394, _default_scale)
FARM_R = Region(384, 63, 1158, 815, _default_scale)
ZAAP_SCROLL_BAR_END_L = Location(1269, 685, _default_scale)
ZAAP_END_SCROLL_C = QColor(190, 226, 0)

# Patterns
READY_BUTTON_P = loadPattern("READY_BUTTON_P.png")
COMBAT_ENDED_POPUP_P = loadPattern("END_COMBAT_P.png")
CREATURE_MODE_OFF_P = loadPattern("CREATURE_MODE_OFF_P.png")
SKIP_TURN_BUTTON_P = loadPattern("SKIP_TURN_BUTTON_P.png")
RESIGN_POPUP_P = loadPattern("RESIGN_POPUP_P.png")
DEFEAT_POPUP_P = loadPattern("DEFEAT_POPUP_P.png")
DISCONNECTED_BOX_P = loadPattern("DISCONNECTED_BOX_P.png")
RECONNECT_BUTTON_P = loadPattern("RECONNECT_BUTTON_P.png")
PLAY_GAME_BUTTON_P = loadPattern("PLAY_GAME_BUTTON_P.png")
CLOSE_POPUP_P = loadPattern("CLOSE_POPUP_P.png")
REDUCE_BOX_P = loadPattern("reduceBox.png")

# bank
BANK_MAN_P = loadPattern("BANK_MAN_P.png")
BANK_MAN_TALK_P = loadPattern("BANK_MAN_TALK_P.png")

# inventory
INVENTAIRE_P = loadPattern("INVENTAIRE.png")
EMPTY_SLOT_INV_P = loadPattern("EMPTY_SLOT_INV_P.png")

# ZAAP
ZAAP_OPEN_P = loadPattern("ZAAP_OPEN_P.png")

# Env Vars
HCELLS = 14.5
VCELLS = 20.5

UP = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, 1)

mapChangeLoc = {
    UP: [
        Region(877, 29, 142, 12, _default_scale),
        Region(492, 29, 141, 11, _default_scale),
        Region(1318, 30, 165, 11, _default_scale)],
    LEFT: [
        Region(335, 349, 14, 126, _default_scale),
        Region(337, 112, 10, 116, _default_scale),
        Region(338, 719, 11, 116, _default_scale)],
    RIGHT: [
        Region(1576, 360, 7, 125, _default_scale),
        Region(1572, 53, 11, 98, _default_scale),
        Region(1572, 752, 12, 100, _default_scale)],
    DOWN: [
        Region(898, 901, 137, 12, _default_scale),
        Region(423, 905, 111, 6, _default_scale),
        Region(1334, 893, 111, 22, _default_scale)]
}

MY_TURN_CHECK_L = Location(1425, 963, _default_scale)
END_COMBAT_CLOSE_L = Location(1251, 737, _default_scale)
MY_TURN_C = QColor(0, 240, 206, 255)
RESIGN_BUTTON_LOC = Location(1443, 1006, _default_scale)
RESIGN_CONFIRM_L = Location(879, 567, _default_scale)
DEFEAT_POPUP_CLOSE_L = Location(1122, 730, _default_scale)
CLOSE_DISCONNECTED_BOX_L = Region(866, 549, 205, 42, _default_scale)
CLOSE_LVL_UP_POPUP_L = Region(336, 573, 46, 32, _default_scale)

# Shortcuts
RAPPEL_POTION_SHORTCUT = "e"
SKIP_TURN_SHORTCUT = 'space'
HAVRE_SAC_SHORTCUT = "h"

ENU_COLOR = [QColor(253, 242, 206), QColor(253, 190, 45), QColor(254, 249, 226), QColor(216, 138, 22)]
SRAM_COLOR = [QColor(61, 56, 150), QColor(251, 241, 191), QColor(33, 34, 88), QColor(227, 218, 173),
              QColor(34, 51, 153)]

FULL_POD_CHECK_L = Location(1266, 1019, _default_scale)
FULL_POD_COLOR = QColor(53, 190, 96)


class ObjColor:
    BOT = ENU_COLOR + SRAM_COLOR
    MOB = [QColor(46, 54, 61), QColor(41, 48, 55)]
    FREE = [QColor(150, 142, 103), QColor(142, 134, 94), QColor(186, 181, 155), QColor(128, 121, 85)]
    OBSTACLE = [QColor(255, 255, 255), QColor(88, 83, 58), QColor(79, 75, 52), QColor(228, 228, 226)]
    DARK = [QColor(0, 0, 0)]
    REACHABLE = [QColor(90, 125, 62), QColor(85, 121, 56), QColor(0, 102, 0), QColor(77, 109, 50)]
    INVOKE = [QColor(218, 57, 45), QColor(255, 244, 221)]
    MY_TURN_COLOR = QColor(252, 200, 0)


class ObjType:
    REACHABLE = QColor(Qt.darkGreen)
    OBSTACLE = QColor(88, 83, 58)
    DARK = Qt.black
    MOB = QColor(Qt.darkBlue)
    BOT = QColor(Qt.darkRed)
    FREE = QColor(142, 134, 94)
    INVOKE = QColor(Qt.yellow)
    UNKNOWN = QColor(Qt.gray)


def findObject(color):
    result = ObjType.UNKNOWN

    if color in ObjColor.OBSTACLE:
        result = ObjType.OBSTACLE

    elif color in ObjColor.FREE:
        result = ObjType.FREE

    elif color in ObjColor.REACHABLE:
        result = ObjType.REACHABLE

    elif color in ObjColor.INVOKE:
        result = ObjType.INVOKE

    elif color in ObjColor.MOB:
        result = ObjType.MOB

    elif color in ObjColor.BOT:
        result = ObjType.BOT

    elif color in ObjColor.DARK:
        result = ObjType.DARK

    return result
