from core.tools.image_processing.InfoBubbleFinder import info_bubble_finder
from core.tools.image_processing.BrightAreaFinder import find_bright_area
from core.tools.image_processing.AreaMatcher import match_areas
from core.tools.image_processing.InfoBubbleReader import read_bubble_text_from_rect

import cv2
import numpy as np
import unittest


class PossibleFightDescriptor:
    def __init__(self, text, area_rect):
        self.lvl = None
        self.xp = None
        self.monsters = []
        self.pixel_rect = area_rect
        self.is_valid = True
        self.parse_text(text)

    def parse_text(self, text: str):
        try:
            lines = text.split("\n")
            if "Niveau" not in lines[0]:
                self.is_valid = False
            self.lvl = int(lines[0][6:])
            running_lvl = 0
            for line in lines[1:]:
                if self.xp is None:
                    if "XP" in line:
                        line = line.replace(" ", "")
                        self.xp = int(line[:-2])
                else:
                    lvl_start = line.rfind('(')
                    lvl_end = line.rfind(')')
                    if lvl_end == -1 or lvl_start == -1:
                        self.is_valid = False
                        continue
                    lvl = int(line[lvl_start + 1:lvl_end])
                    name = line[:lvl_start-1]
                    self.monsters.append({'lvl': lvl, 'name': name})
                    running_lvl += lvl
            if running_lvl != self.lvl:
                self.is_valid = False
        except ValueError:
            self.is_valid = False


def find_fight_on_map(map_pre_z_img: np.ndarray, map_post_z_img: np.ndarray):
    h, w, c = map_pre_z_img.shape
    bubble_height_thresh = int(h / 11)

    bubbles = info_bubble_finder(map_post_z_img)
    bright_areas = find_bright_area(map_pre_z_img, map_post_z_img)

    pairs = match_areas(bubbles, bright_areas)
    fights = []
    for bubble_i, bright_i in pairs:
        if bubbles[bubble_i][3] < bubble_height_thresh:
            continue
        text = read_bubble_text_from_rect(map_post_z_img, bubbles[bubble_i])
        if "Niveau" not in text:
            continue
        fights.append(PossibleFightDescriptor(text=text, area_rect=bright_areas[bright_i]))

    return fights


class TestFightFinder(unittest.TestCase):
    def test_fight_finder1(self):
        img1 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection1_1.png")
        img2 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection1_2.png")
        target = [(470, 1029, 45, 72), (573, 724, 46, 72), (882, 940, 41, 69)]

        fights = find_fight_on_map(img1, img2)

        self.assertEqual(len(fights), 3)
        for f in fights:
            print(f.lvl, f.xp, f.monsters, f.pixel_rect)
            self.assertIn(f.pixel_rect, target)
            self.assertTrue(f.is_valid)

    def test_fight_finder2(self):
        img1 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection2_1.png")
        img2 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection2_2.png")
        # target = [(470, 1029, 45, 72), (573, 724, 46, 72), (882, 940, 41, 69)]

        fights = find_fight_on_map(img1, img2)

        self.assertEqual(len(fights), 1)
        for f in fights:
            print(f.lvl, f.xp, f.monsters, f.pixel_rect)
            # self.assertIn(f.pixel_rect, target)
            self.assertTrue(f.is_valid)



