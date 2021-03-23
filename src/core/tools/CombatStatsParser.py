from core import dofus

import pytesseract
import cv2
import re
import unittest


def read_pa():
    pa_image = dofus.PA_R.capture()
    h, w, c = pa_image.shape
    blue = cv2.threshold(pa_image[:, :, 0], thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
    thresh = blue
    thresh = cv2.resize(thresh, (w * 10, h * 10))
    thresh = cv2.blur(thresh, (7, 7))
    text = pytesseract.image_to_string(thresh, config='--psm 6', lang='fra')
    res = re.findall("(\d+)", text)
    assert len(res) > 0
    return int(res[0])


def read_pm():
    pm_image = dofus.PM_R.capture()
    h, w, c = pm_image.shape
    thresh = cv2.threshold(pm_image[:, :, 0], thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
    thresh = cv2.resize(thresh, (w * 10, h * 10))
    thresh = cv2.blur(thresh, (7, 7))
    text = pytesseract.image_to_string(thresh, config='--psm 6', lang='fra')
    res = re.findall("(\d+)", text)
    assert len(res) > 0
    return int(res[0])


class TestCombatStatsParserMethods(unittest.TestCase):
    def test_pa(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight1.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertTrue(read_pa() == 6)

    def test_pm(self):
        from core import env
        import cv2
        from core.ScaleManager import ScaleManager

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight1.png")
        h, w, c = img.shape
        ScaleManager().set_win_size(w, h)
        env.force_frame(img)

        self.assertTrue(read_pm() == 3)

