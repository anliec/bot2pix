import cv2
import unittest


def info_bubble_finder(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, info_detect = cv2.threshold(gray, thresh=30, maxval=255, type=cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(info_detect, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    selected = []
    for c in contours:
        rect = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if area > 2500 and rect[2] * rect[3] * 0.7 < area:
            selected.append(rect)
    return selected
    # if len(selected) > 0:
    #     x, y, w, h = selected[0]
    #     # add some margin
    #     m = 5
    #     x, y, w, h = x + m, y + m, w - 2 * m, h - 2 * m
    #     crop = img[y:y + h, x:x + w, :]
    #     text = self.read_resources_text(crop)


class TestFindBubbleText(unittest.TestCase):
    def test_find_bubble(self):
        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/map_with_bubble1.png")
        target = [(150, 501, 189, 266), (513, 212, 189, 182), (1198, 682, 161, 125)]

        bubbles = info_bubble_finder(img)

        self.assertEqual(len(bubbles), 3)
        bubbles = sorted(bubbles, key=lambda x: x[0] * 2000 + x[1])
        for b, t in zip(bubbles, target):
            for bi, ti in zip(b, t):
                self.assertAlmostEqual(bi, ti, delta=5)

    def test_find_bubble2(self):
        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fightDetection2_2.png")
        target = [(1054, 146, 207, 266)]

        bubbles = info_bubble_finder(img)

        self.assertEqual(len(bubbles), 1)
        bubbles = sorted(bubbles, key=lambda x: x[0] * 2000 + x[1])
        for b, t in zip(bubbles, target):
            # x, y, w, h = b
            # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
            for bi, ti in zip(b, t):
                self.assertAlmostEqual(bi, ti, delta=5)
        # cv2.imshow("bubbles", img)
        # cv2.waitKey()




