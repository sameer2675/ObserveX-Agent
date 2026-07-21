from config import API_HEARTBEAT_ENDPOINT
from client.client import post


def send_heartbeat(device_id):

    return post(
        API_HEARTBEAT_ENDPOINT,
        {
            "device_id": device_id
        }
    )