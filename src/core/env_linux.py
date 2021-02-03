from core.ScaleManager import ScaleManager

from time import sleep, time
import numpy as np
import pyautogui
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
    print("click at: {},{}".format(x, y))
    pyautogui.click(x=(last_frame_origin.x + x), y=(last_frame_origin.y + y))
    last_frame = None


def press(key):
    global last_frame
    pyautogui.press(key)
    last_frame = None


def release(key):
    global last_frame
    pyautogui.keyUp(key)
    last_frame = None


def _capture(region):
    global last_frame, last_frame_origin, last_frame_time
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
                last_frame_time = time()
                ScaleManager().set_win_size(w, h)
                break
        else:
            print("Unable to find Dofus window!")
            return np.zeros(shape=(region.width(), region.height(), 3), dtype=np.uint8)

    x, y, w, h = region.getRect()

    img = last_frame[y:y+h, x:x+w, :]

    return img


def scroll(clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0):
    pyautogui.scroll(clicks)


