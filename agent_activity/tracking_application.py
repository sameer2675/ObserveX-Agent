import time
from datetime import datetime

from .application_detection import get_active_window_process_name
from .activity import get_employee_activity

from client.client import post
from config import API_ACTIVITY


BREAK_THRESHOLD = 600
BROWSERS = [
    "chrome.exe",
    "msedge.exe",
    "brave.exe",
    "firefox.exe"
]
def tracking_application(device_id):

    current_app = None
    current_title = None
    start_time = None
    active_seconds = 0
    idle_seconds = 0
    break_seconds = 0
    idle_streak = 0
    while True:
        app_info = get_active_window_process_name()

        if not app_info:
            time.sleep(1)
            continue

        app_name = app_info["process_name"]
        window_title = app_info["window_title"]

        status, _ = get_employee_activity()
        if status == "Active":

            active_seconds += 1
            idle_streak = 0
        else:
            idle_streak += 1

            if idle_streak > BREAK_THRESHOLD:
                break_seconds += 1
            else:
                idle_seconds += 1


        if current_app is None:

            current_app = app_name
            current_title = window_title
            start_time = datetime.now()

        elif (
            current_app != app_name
            or current_title != window_title
        ):

            end_time = datetime.now()
            duration = int(
                (end_time - start_time).total_seconds()
            )

            payload = {
                "device_id": device_id,
                "application_name": current_app,
                "window_title": current_title,
                "duration": duration,
                "active_seconds": active_seconds,
                "idle_seconds": idle_seconds,
                "break_seconds": break_seconds
            }

            print("=" * 60)
            print("Application:", current_app)
            print("Title:", current_title)
            print("Duration:", duration)
            print("=" * 60)

            response = post(
                API_ACTIVITY,
                payload
            )
            print(
                "Activity Response:",
                response
            )
            current_app = app_name

            current_title = window_title

            start_time = datetime.now()

            active_seconds = 0
            idle_seconds = 0
            break_seconds = 0
            idle_streak = 0
        time.sleep(1)

if __name__ == "__main__":

    tracking_application()