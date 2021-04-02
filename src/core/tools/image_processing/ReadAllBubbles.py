import cv2
import unittest

from core.tools.image_processing.InfoBubbleFinder import info_bubble_finder
from core.tools.image_processing.InfoBubbleReader import read_bubble_text


def read_all_bubble(img):
    bubbles = info_bubble_finder(img)
    bubble_dict = {}
    for x, y, w, h in bubbles:
        m = 5
        x, y, w, h = x + m, y + m, w - 2 * m, h - 2 * m
        crop = img[y:y + h, x:x + w, :]
        text = read_bubble_text(crop)
        bubble_dict[(x, y, w, h)] = text
    return bubble_dict


class TestFindBubbleText(unittest.TestCase):
    def test_read_all_bubbles(self):
        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/map_with_bubble1.png")
        target = {"Niveau 152\n25 932 XP\nMilimulou (28)\nMilimulou (26)\nMilimulou (24)\nSanglier (28)\n"
                  "Ecurouille (24)\nEcurouille (22)",
                  "Niveau 84\n24 882 XP\nÉcurouille (30)\nPrespic (28)\nPrespic (26)",
                  "Niveau 24\n1 484 XP\nPrespic (24)"}

        bubbles_dict = read_all_bubble(img)

        self.assertEqual(len(bubbles_dict), 3)
        self.assertSetEqual(target, set(bubbles_dict.values()))
