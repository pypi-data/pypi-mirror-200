import requests

class MultiloginClient:
    BASE_URL = "https://api.multiloginapp.com/v2"

    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def get_all_profiles(self):
        url = f"{self.BASE_URL}/profile/getAll"
        response = requests.get(url, headers=self.headers)
        return response.json()
