import requests


class STT:
    def __init__(self, server_url="http://192.168.0.103:8000"):
        self.server_url = server_url

    def process(self, audio):
        files = {"file": audio}
        response = requests.post(f"{self.server_url}/transcribe", files=files)

        if response.status_code == 200:
            transcription = response.json()["text"]
            return transcription
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")