from core.ScaleManager import ScaleManager

from time import sleep, time
import numpy as np
import cv2
import pyautogui
import unittest
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')
from gi.repository import Gtk, Wnck, Gdk, GdkX11


IDE_XID = None
DOFUS_XID = None
last_frame = None
last_frame_origin = None
last_frame_time = None
header_bar_height = None


def focusDofusWindow(account_name=None):
    global DOFUS_XID
    screen = Wnck.Screen.get_default()
    screen.force_update()  # recommended per Wnck documentation
    if not account_name:
        pattern = "Dofus"

    else:
        pattern = account_name
    for win in screen.get_windows():
        if pattern in win.get_name():
            break
    else:
        raise Exception("Unable to find Dofus window with pattern: '{}'".format(pattern))
    DOFUS_XID = win.get_xid()
    # Get time from X11 server
    now = GdkX11.x11_get_server_time(GdkX11.X11Window.lookup_for_display(Gdk.Display.get_default(),
                                                                         GdkX11.x11_get_default_root_xwindow()))
    # Ask to focus Dofus window for keyboard / mouse input
    win.activate(now)


def focusIDEWindow():
    global IDE_XID
    screen = Wnck.Screen.get_default()
    screen.force_update()  # recommended per Wnck documentation
    for win in screen.get_windows():
        if "bot2pix" in win.get_name():
            IDE_XID = win.get_xid()
            break
    # do not focus here, we don't need that for screenshot


def capture(region):
    return _capture(region)


def move(x, y):
    global last_frame, last_frame_origin
    pyautogui.moveTo(last_frame_origin.x + x, last_frame_origin.y + y)
    last_frame = None


def click(x, y):
    global last_frame, last_frame_origin
    pyautogui.click(x=(last_frame_origin.x + x), y=(last_frame_origin.y + y))
    last_frame = None


def press(key):
    global last_frame
    pyautogui.keyDown(key)
    last_frame = None


def release(key):
    global last_frame
    pyautogui.keyUp(key)
    last_frame = None


def _capture(region):
    global last_frame, last_frame_origin, last_frame_time, header_bar_height
    if last_frame is None or last_frame_time + 2.0 < time():
        window = Gdk.get_default_root_window()
        screen = window.get_screen()
        for i, win in enumerate(screen.get_window_stack()):
            if win.get_xid() == DOFUS_XID:
                pb = Gdk.pixbuf_get_from_window(win, *win.get_geometry())
                last_frame_origin = win.get_origin()
                w, h, c, r = pb.get_width(), pb.get_height(), pb.get_n_channels(), pb.get_rowstride()
                f = np.frombuffer(pb.get_pixels(), dtype=np.uint8)
                if f.shape[0] == w * c * h:
                    last_frame = f.reshape((h, w, c))
                else:
                    b = np.zeros((h, w * c), dtype=np.uint8)
                    for j in range(h):
                        b[j, :] = f[r * j:r * j + w * c]
                    last_frame = b.reshape((h, w, c))
                last_frame = cv2.cvtColor(last_frame, cv2.COLOR_RGB2BGR)
                last_frame_time = time()
                if header_bar_height is None:
                    compute_header_height(last_frame)
                ScaleManager().set_win_size(w, h, header_bar_height)
                break
        else:
            print("Unable to find Dofus window!")
            return np.zeros(shape=(region.width(), region.height(), 3), dtype=np.uint8)

    if region is None:
        return last_frame

    x, y, w, h = region.getRect()
    img = last_frame[y:y+h, x:x+w, :]
    return img


def force_frame(frame):
    global last_frame, last_frame_origin, last_frame_time
    last_frame = frame
    last_frame_time = time()
    compute_header_height(frame)
    h, w, c = frame.shape
    ScaleManager().set_win_size(w, h, header_bar_height)


def scroll(clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0):
    pyautogui.scroll(clicks)


def compute_header_height(img):
    global header_bar_height
    x = 10
    min_y = 0
    max_y = 128
    # assert (img[max_y, x, :] == 0).all(), "To ensure bot functionality, please disable side map display in Dofus " \
    #                                       "settings"
    if (img[min_y, x, :] == 0).all():
        header_bar_height = min_y
        return min_y
    while min_y + 1 < max_y:
        p = int((min_y + max_y) / 2)
        if (img[p, x, :] == 0).all():
            max_y = p
        else:
            min_y = p
    header_bar_height = max_y
    return max_y


class EnvLinuxMethods(unittest.TestCase):
    def test_fight1(self):
        import cv2

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight1.png")
        self.assertTrue(compute_header_height(img) == 0)

    def test_fight2_header(self):
        import cv2

        img = cv2.imread("/home/nicolas/Documents/Programation/Python/bot2pix/TestData/img/fight2_header.png")
        self.assertEqual(31, compute_header_height(img))


