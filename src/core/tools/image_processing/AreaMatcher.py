import numpy as np
from collections import defaultdict
import unittest


def are_rect_close(rect1, rect2, m=10):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    x1, y1, x2, y2 = [v - m for v in [x1, y1, x2, y2]]
    w1, h1, w2, h2 = [v + (2 * m) for v in [w1, h1, w2, h2]]

    if x1 <= x2 + w2 and x1 + w1 >= x2:
        if y1 <= y2 + h2 and y1 + h1 >= y2:
            return True
    return False


def match_areas(bubble_rect_list, bright_rect_list):
    matches12 = defaultdict(set)
    matches21 = defaultdict(set)

    for i1, rect1 in enumerate(bubble_rect_list):
        for i2, rect2 in enumerate(bright_rect_list):
            if are_rect_close(rect1, rect2):
                matches12[i1].add(i2)
                matches21[i2].add(i1)

    pairs = []
    change = True
    while change:
        change = False
        for i1, matches2 in matches12.items():
            if len(matches2) == 1:
                i2 = matches2.pop()
                pairs.append((i1, i2))
                # remove all i2 from possible matches
                for i2match in matches21[i2]:
                    i2set = matches12[i2match]
                    if i2 in i2set:
                        i2set.remove(i2)
                del matches21[i2]
                change = True
                break
        for i2, matches1 in matches21.items():
            if len(matches1) == 1:
                i1 = matches1.pop()
                pairs.append((i1, i2))
                # remove all i1 from possible matches
                for i1match in matches12[i1]:
                    i1set = matches21[i1match]
                    if i1 in i1set:
                        i1set.remove(i1)
                del matches12[i1]
                change = True
                break
    return pairs


class TestAreaMatcher(unittest.TestCase):
    def test_area_rect_close(self):

        self.assertTrue(are_rect_close((10, 10, 10, 10), (10, 10, 10, 10), 1))
        self.assertTrue(are_rect_close((10, 10, 10, 10), (0, 0, 10, 10), 1))
        self.assertTrue(are_rect_close((10, 10, 10, 10), (10, 0, 10, 10), 1))
        self.assertTrue(are_rect_close((10, 10, 10, 10), (0, 10, 10, 10), 1))
        self.assertTrue(are_rect_close((10, 10, 10, 10), (0, 20, 10, 10), 1))
        self.assertTrue(are_rect_close((10, 10, 10, 10), (20, 0, 10, 10), 1))
        self.assertTrue(are_rect_close((10, 10, 10, 10), (20, 20, 10, 10), 1))

        self.assertFalse(are_rect_close((10, 10, 10, 10), (0, 0, 5, 5), 1))

    def test_match_areas_basic(self):
        a = [(0, 0, 10, 10), (50, 50, 10, 10)]
        b = [(3, 12, 4, 4), (53, 63, 4, 4)]

        self.assertTrue(are_rect_close(a[0], b[0]))
        self.assertTrue(are_rect_close(a[1], b[1]))
        self.assertFalse(are_rect_close(a[0], b[1]))
        self.assertFalse(are_rect_close(a[1], b[0]))

        p = match_areas(a, b)

        self.assertEqual(len(p), 2)
        self.assertIn((0, 0), p)
        self.assertIn((1, 1), p)

    def test_match_areas_easy(self):
        a = [(400, 400, 100, 100), (500, 500, 100, 100)]
        b = [(451, 510, 40, 40), (530, 613, 40, 40)]

        self.assertTrue(are_rect_close(a[0], b[0]))
        self.assertTrue(are_rect_close(a[1], b[1]))
        self.assertFalse(are_rect_close(a[0], b[1]))
        self.assertTrue(are_rect_close(a[1], b[0]))

        p = match_areas(a, b)

        self.assertEqual(len(p), 2)
        self.assertIn((0, 0), p)
        self.assertIn((1, 1), p)

    def test_match_areas_easy2(self):
        a = [(400, 400, 100, 100), (500, 500, 100, 100)]
        b = [(451, 510, 40, 40), (530, 613, 40, 40)]

        self.assertTrue(are_rect_close(a[0], b[0]))
        self.assertTrue(are_rect_close(a[1], b[1]))
        self.assertFalse(are_rect_close(a[0], b[1]))
        self.assertTrue(are_rect_close(a[1], b[0]))

        p = match_areas(a, b[::-1])

        self.assertEqual(len(p), 2)
        self.assertIn((0, 1), p)
        self.assertIn((1, 0), p)

