import requests
import json


class FirebaseHelper:
    def __init__(self):
        self.db_url = "https://chat-app-63bb3-default-rtdb.firebaseio.com/chat"

    def put_data(self, data, path):
        """
        Uses the firebase PUT API to insert data to the given path
        :param data: data to be inserted
        :param path: realtime db path
        """
        url = f"{self.db_url}{path}.json"
        response = requests.put(url=url, data=json.dumps(data, default=str))
        return response.status_code