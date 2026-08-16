import time
from pynput import mouse

latest_mouse_activity = time.time()

def on_move(x, y):
    global latest_mouse_activity
    latest_mouse_activity = time.time()
def on_click(x, y, button, pressed):
    global latest_mouse_activity
    if pressed:
        latest_mouse_activity = time.time()
def on_scroll(x, y, dx, dy):
    global latest_mouse_activity
    latest_mouse_activity = time.time()

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
mouse_listener.daemon = True
mouse_listener.start()
def mouse_activity():
    return latest_mouse_activity