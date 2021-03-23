from core import dofus

import numpy as np
import unittest

COUNT_DOWN_TIMER_COLOR = np.array((0, 200, 252))
READY_BUTTON_ACTIVE = np.array((0, 240, 206))
READY_BUTTON_DISABLED = np.array((0, 143, 124))


def is_ready_button_enabled():
    end_turn_button = dofus.READY_R.capture()
    return np.sum(end_turn_button == READY_BUTTON_ACTIVE) > (dofus.READY_R.area() / 10)


def is_ready_button_disabled():
    end_turn_button = dofus.READY_R.capture()
    return np.sum(end_turn_button == READY_BUTTON_DISABLED) > (dofus.READY_R.area() / 10)


def is_ready_button_visible():
    return is_ready_button_enabled() or is_ready_button_disabled()


class TestCombatManagerMethods(unittest.TestCase):
    def test_fight1(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight1.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertTrue(is_ready_button_enabled())
        self.assertFalse(is_ready_button_disabled())
        self.assertTrue(is_ready_button_visible())

    def test_fight2(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight2.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertTrue(is_ready_button_enabled())
        self.assertFalse(is_ready_button_disabled())
        self.assertTrue(is_ready_button_visible())

    def test_fight3(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight3.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertTrue(is_ready_button_enabled())
        self.assertFalse(is_ready_button_disabled())
        self.assertTrue(is_ready_button_visible())

    def test_fight_not_our_turn(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight_not_our_turn.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertFalse(is_ready_button_enabled())
        self.assertTrue(is_ready_button_disabled())
        self.assertTrue(is_ready_button_visible())

    def test_pos_selection(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/startPosSelection.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertTrue(is_ready_button_enabled())
        self.assertFalse(is_ready_button_disabled())
        self.assertTrue(is_ready_button_visible())

    def test_fight_end(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightEnd.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertFalse(is_ready_button_enabled())
        self.assertFalse(is_ready_button_disabled())
        self.assertFalse(is_ready_button_visible())











