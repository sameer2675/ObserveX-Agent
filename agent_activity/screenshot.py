import os
from datetime import datetime
import mss
from PIL import Image
import time
from .application_detection import get_active_window_process_name
from .browser_title import strip_browser_suffix
from client.screenshot import upload_screenshot
from config import SERVER_URL, API_UPLOAD_SCREENSHOT_ENDPOINT
APP_DATA = os.path.join(os.environ["LOCALAPPDATA"], "ObserveXAgent")
SAVING_PATH = os.path.join( APP_DATA, "screenshots")
os.makedirs(SAVING_PATH, exist_ok=True)
def capture_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVING_PATH, f"screenshot_{timestamp}.png")
    with mss.mss() as sct:
        monitor = sct.monitors[1]  
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        img.save(filename)
    return filename  
def track_screenshot_with_active_window(device_id):
    last_screenshot_process = None
    last_screenshot_title = None
    print("Waiting for active window changes to capture screenshots...")
    while True:
        try:
            app_info = get_active_window_process_name()
            if app_info is None:
                time.sleep(1)
                continue
            print(app_info)
            current_process = app_info["process_name"]
            current_title = strip_browser_suffix(app_info["process_name"], app_info["window_title"])
            if (current_process != last_screenshot_process) or (current_title != last_screenshot_title):
                screenshot_path = capture_screenshot()
                response = upload_screenshot(
                    {"device_id": device_id,
                     "window_title": current_title,
                     "application_name": current_process},
                     screenshot_path)
                print(f"Upload response: {response}")
                print(f"Captured screenshot for {current_process} - {current_title}: {screenshot_path}")
                last_screenshot_process = current_process
                last_screenshot_title = current_title
                if response and response.get("status") == "success":
                   os.remove(screenshot_path)
                   print("Screenshot uploaded and local copy deleted.")
            time.sleep(1) 
        except Exception as e:
            print(f"Error in tracking screenshots: {e}")
            time.sleep(5)  
def capturing_screenshot(device_id):
    try:
        app_info = get_active_window_process_name()
        if app_info is None:
            print("No active window detected. Skipping screenshot capture.")
            return
        current_process = app_info["process_name"]
        current_title = strip_browser_suffix(app_info["process_name"], app_info["window_title"])
        screenshot_path = capture_screenshot()
        response = upload_screenshot(
            {"device_id": device_id,
             "window_title": current_title,
             "application_name": current_process},
             screenshot_path)
        print(f"Upload response: {response}")
        print(f"Captured screenshot for {current_process} - {current_title}: {screenshot_path}")
        if response and response.get("status") == "success":
            os.remove(screenshot_path)
            print("Screenshot uploaded and local copy deleted.")
    except Exception as e:
        print(f"Error in capturing screenshot: {e}")
if __name__ == "__main__":
    print("Starting screenshot tracking...")