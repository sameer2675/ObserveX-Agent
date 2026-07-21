import time
from pynput import keyboard

latest_keyboard_activity = time.time()

def on_press(key):
    global latest_keyboard_activity
    latest_keyboard_activity = time.time()

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.daemon = True
keyboard_listener.start()

def keyboard_activity():
    return latest_keyboard_activity
