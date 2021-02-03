from PyQt5.QtCore import QRect
import sys


if sys.platform == 'win32' or sys.platform == 'cygwin':
    import core.env_win as env

    focusDofusWindow = env.focusDofusWindow
    focusIDEWindow = env.focusIDEWindow
    capture = env.capture
    move = env.move
    click = env.click
    press = env.press
    release = env.release
    scroll = env.scroll
elif sys.platform == 'linux':
    import core.env_linux as env

    focusDofusWindow = env.focusDofusWindow
    focusIDEWindow = env.focusIDEWindow
    capture = env.capture
    move = env.move
    click = env.click
    press = env.press
    release = env.release
    scroll = env.scroll


if __name__ == "__main__":
    for k in range(81):
        r = QRect(100, 100, 100, 100)
        capture(r)
