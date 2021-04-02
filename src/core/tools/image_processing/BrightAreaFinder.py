import cv2
import numpy as np
import unittest


def find_bright_area(img_base: np.ndarray, img_bright: np.ndarray):
    img_base_gray = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
    img_bright_gray = cv2.cvtColor(img_bright, cv2.COLOR_BGR2GRAY)

    h, w, c = img_base.shape
    area_thresh = w // 3

    brighter = (img_base_gray < img_bright_gray).astype(np.uint8) * 255

    contours, _ = cv2.findContours(brighter, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    selected = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            rect = cv2.boundingRect(c)
            selected.append(rect)
    return selected


# if __name__ == '__main__':
#     from core import env, dofus
#     import time
#     env.focusDofusWindow("Pif-Protect")
#     # capture the whole screen to initialise scale manager
#     env.capture(None)
#     im1 = env.capture(dofus.COMBAT_R)
#     env.press('z')
#     time.sleep(0.1)
#     im2 = env.capture(dofus.COMBAT_R)
#     env.release('z')
#     cv2.imwrite("/tmp/im1.png", im1)
#     cv2.imwrite("/tmp/im2.png", im2)

class TestFindBrightArea(unittest.TestCase):
    def test_bright_area_1(self):
        img1 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection1_1.png")
        img2 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection1_2.png")
        target = [(470, 1029, 45, 72), (525, 515, 42, 77), (573, 724, 46, 72), (882, 940, 41, 69),
                  (1517, 436, 108, 185)]

        areas = find_bright_area(img1, img2)

        self.assertEqual(len(areas), 5)
        areas = sorted(areas, key=lambda x: x[0] * 2000 + x[1])
        for b, t in zip(areas, target):
            for bi, ti in zip(b, t):
                self.assertAlmostEqual(bi, ti, delta=5)

    def test_bright_area_2(self):
        img1 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection2_1.png")
        img2 = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection2_2.png")
        # target = [(470, 1029, 45, 72), (525, 515, 42, 77), (573, 724, 46, 72), (882, 940, 41, 69),
        #           (1517, 436, 108, 185)]

        areas = find_bright_area(img1, img2)

        self.assertEqual(len(areas), 1)
        # areas = sorted(areas, key=lambda x: x[0] * 2000 + x[1])
        # for b, t in zip(areas, target):
        #     for bi, ti in zip(b, t):
        #         self.assertAlmostEqual(bi, ti, delta=5)

        for a in areas:
            x, y, w, h = a
            cv2.rectangle(img2, (x, y), (x+w, y+h), (255, 0, 0), 3)
        cv2.imshow("area", img2)
        cv2.waitKey()

