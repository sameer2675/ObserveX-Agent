import requests
from config import SERVER_URL

def post(endpoint, data):
    try:
        response = requests.post(
            SERVER_URL + endpoint,
            json=data,
            timeout=10
        )
        print(f"\nPOST -> {endpoint}")
        print("Status:", response.status_code)
        if response.status_code in (200, 201):
            return response.json()
        print(response.text)
        return None
    except Exception as e:
        print("POST ERROR:", e)
        return None
def upload(endpoint, data, image_path):
    try:
        with open(image_path, "rb") as f:

            files = {
                "image": f}
            response = requests.post(
                SERVER_URL + endpoint,
                data=data,
                files=files,
                timeout=30)
        print(f"\nUPLOAD -> {endpoint}")
        print("Status:", response.status_code)
        if response.status_code in (200, 201):
            return response.json()
        print(response.text)
        return None
    except Exception as e:
        print("UPLOAD ERROR:", e)
        return None