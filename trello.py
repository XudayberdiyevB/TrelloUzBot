import requests
import json

from environs import Env

env = Env()
env.read_env()


class TrelloManager:
    KEY = env("TRELLO_KEY")
    TOKEN = env("TRELLO_TOKEN")

    def __init__(self, username):
        self.username = username

    @staticmethod
    def base_headers():
        return {
            "Accept": "application/json"
        }

    def credentials(self):
        return {
            'key': self.KEY,
            'token': self.TOKEN
        }

    def get_boards(self):
        url = f"https://api.trello.com/1/members/{self.username}/boards"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)
