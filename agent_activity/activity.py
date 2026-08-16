import time
from .keyboard import keyboard_activity
from .mouse import mouse_activity
IDLE_TIME = 300 

def get_employee_activity():
    keyboard_time = keyboard_activity()
    mouse_time = mouse_activity()
    latest = max(keyboard_time, mouse_time)
    idle_duration = time.time() - latest
    if idle_duration > IDLE_TIME:
        idle_seconds = round(idle_duration)
        return "Idle", idle_seconds
    else:
        return "Active", round(idle_duration)