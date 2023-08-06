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
        """
        Retrieve a list of all profiles in the Multilogin account.

        Returns:
            list: A list of profiles.
        """
        url = f"{self.BASE_URL}/profile/getAll"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_profile_by_id(self, profile_id):
        """
        Retrieve a profile by its ID.

        Args:
            profile_id (str): The ID of the profile to retrieve.

        Returns:
            dict: The profile data.
        """
        return self.call_formated_url('/profile/getById', profile_id)

    def create_profile(self, profile_data):
        """
        Create a new profile in the Multilogin account.

        Args:
            profile_data (dict): A dictionary containing the profile data. Example:
                {
                    "name": "Profile Name",
                    "browserType": "mimic",
                    "os": "Windows",
                    "resolution": "1920x1080"
                }

        Returns:
            dict: The created profile data.
        """
        url = f"{self.BASE_URL}/profile/create"
        response = requests.post(url, json=profile_data, headers=self.headers)
        return response.json()

    def update_profile(self, profile_id, profile_data):
        """
        Update an existing profile.

        Args:
            profile_id (str): The ID of the profile to update.
            profile_data (dict): A dictionary containing the updated profile data. Example:
                {
                    "name": "Updated Profile Name",
                    "resolution": "1280x720"
                }

        Returns:
            dict: The updated profile data.
        """
        url = f"{self.BASE_URL}/profile/updateById"
        payload = {"id": profile_id, **profile_data}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def delete_profile(self, profile_id):
        """
        Delete a profile by its ID.

        Args:
            profile_id (str): The ID of the profile to delete.

        Returns:
            dict: A dictionary containing the result of the deletion.
        """
        return self.call_formated_url('/profile/deleteById', profile_id)

    def start_profile(self, profile_id):
        """
        Start a profile by its ID.

        Args:
            profile_id (str): The ID of the profile to start.

        Returns:
            dict: A dictionary containing the result of the profile start operation.
        """
        return self.call_formated_url('/profile/startById', profile_id)

    def stop_profile(self, profile_id):
        """
        Stop a profile by its ID.

        Args:
            profile_id (str): The ID of the profile to stop.

        Returns:
            dict: A dictionary containing the result of the profile stop operation.
        """
        return self.call_formated_url('/profile/stopById', profile_id)

    def call_formated_url(self, arg0, profile_id):
        url = f"{self.BASE_URL}{arg0}"
        payload = {"id": profile_id}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()


