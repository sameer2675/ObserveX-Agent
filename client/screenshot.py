from config import API_UPLOAD_SCREENSHOT_ENDPOINT
from client.client import upload
def upload_screenshot(data, image_path):
    return upload(API_UPLOAD_SCREENSHOT_ENDPOINT,data,
        image_path)