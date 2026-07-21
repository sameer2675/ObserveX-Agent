import psutil
import win32gui
import win32process

BROWSERS = [
    "brave.exe",
    "chrome.exe",
    "firefox.exe",
    "msedge.exe",
    "opera.exe",
]

def get_browser():
    try:
        current_window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(current_window)
        _, process_id = win32process.GetWindowThreadProcessId(current_window)
        process = psutil.Process(process_id)
        process_name = process.name().lower()
        if process_name in BROWSERS:
            return {
                "browser": process_name,
                "window_title": title,
            }
        return None
    except Exception as e:
        print(f"Error getting browser: {e}")
        return None