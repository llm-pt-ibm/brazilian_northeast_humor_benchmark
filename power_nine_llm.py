import requests
import json

class PowerNineModel:
    def __init__(self, model_name: str, url: str, hf_token: str, api_key: str):
        self.model_name = model_name.split('/')[1] if '/' in model_name else model_name
        self.model_id = model_name
        self.hf_token = hf_token
        self.url = url
        self.headers = {"Content-Type": "application/json", "x-api-key": api_key}
        payload = {"model_name": model_name, "hf_token": hf_token}
        requests.post(f"{url}/load_model", headers=self.headers, json=payload)
        
    def generate(self, prompt: str) -> str:
        payload = {"prompt": prompt, "model_name": self.model_id, "hf_token": self.hf_token}
        resp = requests.post(f"{self.url}/generate", headers=self.headers, json=payload)
        resp = json.loads(resp.content.decode())

    def unload_model(self):
        requests.post(f"{self.url}/unload_model", headers=self.headers)