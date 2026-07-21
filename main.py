import time
import threading
import traceback
from storage.register import load_registration_data
from agent_activity.browser_listener import start_browser_listener
from client.heartbeat import send_heartbeat
from config import HEARTBEAT_INTERVAL
from agent_activity.tracking_application import tracking_application

def main():
    try:
        print("========== MAIN STARTED ==========")

        registration = load_registration_data()
        print(registration)

        if registration is None:
            print("Agent not registered.")
            return
        device_id = registration["device_id"]
        activity_thread = threading.Thread(
            target=tracking_application,
            args=(device_id,),
            daemon=True
        )
        activity_thread.start()
        browser_thread = threading.Thread(
            target=start_browser_listener,
            args=(device_id,),
            daemon=True
        )
        browser_thread.start()
        print("Browser listener started")
        while True:
            response = send_heartbeat(device_id)
            print(response)
            time.sleep(HEARTBEAT_INTERVAL)
    except Exception:
        with open("main_crash.log", "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise
if __name__ == "__main__":
    main()