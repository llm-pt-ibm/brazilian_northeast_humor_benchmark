import requests
from typing import List, Union

class IBMCloudCustomModel:
    def __init__(self, model_name: str, api_key: str, deployment_url: str):
        self.model_name = model_name
        self.api_key = api_key
        self.deployment_url = deployment_url
        self.token = self._get_token()

    def _get_token(self) -> str:
        response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"apikey={self.api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def generate(self, prompt: str, max_new_tokens: int = 512, temperature: float = 0.7) -> str:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature
            }
        }

        response = requests.post(
            self.deployment_url,
            headers=headers,
            json=payload
        )

        try:
            response.raise_for_status()
            return response.json()["results"][0]["generated_text"]
        except requests.exceptions.HTTPError as e:
            print("Erro na requisição:", response.text)
            raise e