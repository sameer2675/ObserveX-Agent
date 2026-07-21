from config import API_ACTIVITY
from client.client import post


def send_activity(data):
    return post(API_ACTIVITY, data)