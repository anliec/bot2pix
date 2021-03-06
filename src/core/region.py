import collections
import sys
import threading
import random
from time import perf_counter, sleep
import cv2
import numpy as np
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from core import utils
from core.ScaleComputer import ScaleComputer
from core.ScaleManager import ScaleManager
from gui import Overlay
import core.env as env

FOREVER = 60 * 60 * 24 * 1.


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook


def withTimeOut(fn):
    def wrapped(self, *args, timeout=FOREVER, rate=3):
        self.stopWait.clear()
        start = perf_counter()
        while not self.stopWait.is_set() and perf_counter() - start < timeout:
            s = perf_counter()
            r = fn(self, *args)
            if r:
                return r
            rest = (1 / rate) - perf_counter() + s
            sleep(rest if rest > 0 else 0)
        return None, None
    return wrapped


class Location(QPoint):
    def __init__(self, x, y, scale: ScaleComputer, absolute_coordinate=False):
        super(Location, self).__init__(x, y)
        self.base_scale = scale
        self.base_rect = x, y
        self.absolute_coordinate = absolute_coordinate
        # register ourself so we can be scaled when needed
        ScaleManager().register(self)

    def rescale(self, new_scale: ScaleComputer):
        x, y = new_scale.rescale(x=self.base_rect[0],
                                 y=self.base_rect[1],
                                 original_scale=self.base_scale,
                                 just_scale=self.absolute_coordinate)
        self.setX(x)
        self.setY(y)

    def click(self):
        env.click(self.x(), self.y())

    def getpixel(self):
        bi = env.capture(self)
        ni = cv2.cvtColor(bi, cv2.COLOR_RGB2BGR)
        return QColor(*bi[0, 0])

    def width(self):
        # To allow a Location to be given to env.capture
        return 1

    def height(self):
        # To allow a Location to be given to env.capture
        return 1

    def getRect(self):
        # To allow a Location to be given to env.capture
        return self.x(), self.y(), 1, 1


class Region(QRect):

    def __init__(self, x, y, w, h, scale: ScaleComputer, absolute_coordinate=False):
        """
        :param x: x coordinate of the top left corner of the rectangle
        :param y: y coordinate of the top left corner of the rectangle
        :param w: width of the rectangle
        :param h: height of the rectangle
        :param scale: scale at which the coordinate are true
        :param absolute_coordinate: True if the coordinate are relative to the top left corner and not the 4:3
        central area (for the map coordinate for example)
        """
        super(Region, self).__init__(x, y, w, h)
        self.bi = None
        self.stopWait = threading.Event()
        self.base_scale = scale
        self.base_rect = x, y, w, h
        self.absolute_coordinate = absolute_coordinate
        # register ourself so we can be scaled when needed
        ScaleManager().register(self)

    def rescale(self, new_scale: ScaleComputer):
        x, y, w, h = new_scale.rescale_rect(x=self.base_rect[0],
                                            y=self.base_rect[1],
                                            w=self.base_rect[2],
                                            h=self.base_rect[3],
                                            original_scale=self.base_scale,
                                            just_scale=self.absolute_coordinate)
        self.setCoords(x, y, x + w, y + h)
        if self.bi is not None:
            # if we had a capture, update it to the new scale
            self.capture(gray=not (len(self.bi.shape) == 3 and self.bi.shape[2] == 3))

    def area(self):
        return self.width() * self.height()

    @withTimeOut
    def waitAppear(self, pattern, threshold=0.7):
        self.stopWait.clear()
        match = self.find(pattern, threshold)
        if match:
            return match

    @withTimeOut
    def waitAny(self, patterns, threshold=0.7):
        match, idx = self.findAny(patterns, threshold)
        if match:
            return match, idx

    @withTimeOut
    def waitVanish(self, pattern, threshold=0.9):
        match = self.find(pattern, threshold)
        if not match:
            return pattern, match

    def waitChange(self, timeout=FOREVER, nbr_pix=1):
        self.stopWait.clear()
        start = perf_counter()
        initial = env.capture(self)
        while not self.stopWait.is_set() and perf_counter() - start < timeout:
            pix_diff = (initial != env.capture(self)).any(axis=2).sum()
            if pix_diff > nbr_pix:
                return True
            sleep(0.01)
        return False

    def findAnyAll(self, patterns, threshold=0.7, shuffle=False):
        ans = []
        self.capture()
        if shuffle:
            random.shuffle(patterns)
        for pattern in patterns:
            result = self.findAll(pattern, threshold, capture=False)
            for r in result:
                if not utils.isAdjacent(ans, r):
                    ans.append(r)
        return ans

    def findAny(self, patterns, threshold=0.7, shuffle=False):
        self.capture()
        if shuffle:
            random.shuffle(patterns)
        for idx, pattern in enumerate(patterns):
            match = self.find(pattern, threshold, capture=False)
            if match:
                return match, idx
        return None, None

    def waitAnimationEnd(self, timeout=FOREVER):
        self.stopWait.clear()
        lookup_int = 5
        clip = collections.deque()
        for frame in self.stream(timeout):
            if len(clip) > lookup_int:
                if not utils.inMotion(clip):
                    return True
                clip.popleft()
            clip.append(frame)
        return False

    def capture(self, gray=False):
        self.bi = env.capture(self)
        if gray:
            self.bi = cv2.cvtColor(self.bi, cv2.COLOR_RGB2GRAY)
        return self.bi

    def stream(self, interval=FOREVER):
        s = perf_counter()
        while perf_counter() - s < interval:
            yield cv2.cvtColor(env.capture(self), cv2.COLOR_RGB2GRAY)

    def findAll(self, pattern, threshold=0.7, grayscale=True, capture=True):
        matches = []
        if capture:
            self.capture()
        if grayscale:
            cvImage = cv2.cvtColor(self.bi, cv2.COLOR_BGR2GRAY)
            pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)
        else:
            cvImage = cv2.cvtColor(self.bi, cv2.COLOR_RGB2BGR)
            pattern = cv2.cvtColor(pattern, cv2.COLOR_RGB2BGR)
        h, w = pattern.shape[:2]
        result = cv2.matchTemplate(cvImage, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        bestx, besty = max_loc
        if max_val >= threshold:
            matches.append(Region(self.x() + bestx, self.y() + besty, w, h))
        for dx, dy in zip(*loc[::-1]):
            r = Region(self.x() + dx, self.y() + dy, w, h)
            if not utils.isAdjacent(matches, r):
                matches.append(r)
        return matches

    def find(self, pattern, threshold=0.7, grayscale=True, capture=True):
        if capture:
            self.capture()
        if grayscale:
            cvImage = cv2.cvtColor(self.bi, cv2.COLOR_BGR2GRAY)
            pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)
        else:
            cvImage = cv2.cvtColor(self.bi, cv2.COLOR_RGB2BGR)
            pattern = cv2.cvtColor(pattern, cv2.COLOR_RGB2BGR)
        h, w = pattern.shape[:2]
        result = cv2.matchTemplate(cvImage, pattern, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        bestx, besty = max_loc
        if max_val >= threshold:
            return Region(self.x() + bestx, self.y() + besty, w, h)
        else:
            return None

    def highlight(self, secs):
        app = QApplication(sys.argv)
        self.overlay = Overlay()
        self.overlay.highlight(self, secs)
        app.exec_()

    def click(self, x=None, y=None):
        if x is None or y is None:
            env.click(self.center().x(), self.center().y())
        else:
            env.click(self.x() + x, self.y() + y)

    def getpixel(self, x, y):
        return tuple(self.bi[y, x])

    def hover(self):
        env.move(self.center().x(), self.center().y())

    def nearBy(self, w, h):
        return Region(self.center().x() - w / 2, self.center().y() - h / 2, w, h)

    def scroll(self, clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0):
        self.hover()
        env.scroll(clicks, delta_x, delta_y, delay_between_ticks)


