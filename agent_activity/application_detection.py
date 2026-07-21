import win32gui
import win32process
import psutil


def get_active_window_process_name():
    try:
        current_window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(current_window)
        _, process_id = win32process.GetWindowThreadProcessId(current_window)
        process = psutil.Process(process_id)
        return {
            "process_name": process.name(),
            "window_title": title,
            "pid": process_id
        }
    except Exception as e:
        print(f"Error getting active window process name: {e}")
        return None