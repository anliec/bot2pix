import cv2
import pytesseract
import unittest


def read_bubble_text_from_rect(map_image, bubble_rect, m=5):
    x, y, w, h = bubble_rect
    x, y, w, h = x + m, y + m, w - (2 * m), h - (2 * m)
    crop = map_image[y:y + h, x:x + w, :]
    return read_bubble_text(crop)


def read_bubble_text(crop_image):
    h, w, c = crop_image.shape
    crop_red = cv2.threshold(crop_image[:, :, 2], thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
    crop = crop_red
    crop = cv2.resize(crop, (w * 10, h * 10))
    crop = cv2.blur(crop, (7, 7))
    text = pytesseract.image_to_string(crop, config='--psm 6', lang='fra')
    text = text.replace('}', ')')
    text = text.replace('{', '(')
    return text[:-2]


class TestReadBubbleText(unittest.TestCase):
    def test_fight_bubble1(self):
        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/bubbleFight1.png")
        target = "Niveau 152\n25 932 XP\nMilimulou (28)\nMilimulou (26)\nMilimulou (24)\nSanglier (28)\n" \
                 "Ecurouille (24)\nEcurouille (22)"

        text = read_bubble_text(img)

        self.assertEqual(len(target), len(text))
        for c1, c2 in zip(text, target):
            self.assertEqual(c2, c1)

    def test_fight_bubble2(self):
        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/bubbleFight2.png")
        target = "Niveau 84\n24 882 XP\nÉcurouille (30)\nPrespic (28)\nPrespic (26)"

        text = read_bubble_text(img)
        
        self.assertEqual(len(target), len(text))
        for c1, c2 in zip(text, target):
            self.assertEqual(c2, c1)

    def test_fight_bubble3(self):
        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/bubbleFight3.png")
        target = "Niveau 24\n1 484 XP\nPrespic (24)"

        text = read_bubble_text(img)

        self.assertEqual(len(target), len(text))
        for c1, c2 in zip(text, target):
            self.assertEqual(c2, c1)


