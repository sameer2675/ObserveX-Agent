import time
import socket
import json
from client.client import post
from config import API_BROWSER_ACTIVITY
from .screenshot import capturing_screenshot
HOST = "127.0.0.1"
PORT = 5055
def start_browser_listener(device_id):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Browser listener started")

    while True:

        print("Waiting for browser connection...")

        conn, addr = server.accept()

        print("CONNECTED:", addr)

        data = conn.recv(4096)

        print("RAW:", data)

        if data:

            browser_data = json.loads(data.decode())

            print("====================")
            print("Browser Activity")
            print(browser_data)
            print("====================")

            payload = {
                "device_id": device_id,
                "url": browser_data.get("url"),
                "title": browser_data.get("title"),
                "tab_id": browser_data.get("tabId"),
                "window_id": browser_data.get("windowId"),
            }

            response = post(API_BROWSER_ACTIVITY, payload)

            print("Server Response:", response)
            if response.get("take_screenshot") :
                print("Taking screenshot due to browser activity")
                capturing_screenshot(device_id)

        conn.close()