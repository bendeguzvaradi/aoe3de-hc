import pyautogui
import time


def track_mouse_coordinates():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"X: {x}, Y: {y}", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        pass