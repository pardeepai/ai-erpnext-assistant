import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Explicitly find the .env file in the project root (ai-erpnext-assistant/)
# client.py is in ai-erpnext-assistant/app/erpnext/client.py -> go up 3 levels to project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class ERPNextClient:
    def __init__(self):
        self.base_url = os.getenv("ERPNEXT_URL") or os.getenv("ERP_URL")
        self.api_key = (
            os.getenv("ERPNEXT_API_KEY") 
            or os.getenv("API_KEY")
        )
        self.api_secret = (
            os.getenv("ERPNEXT_API_SECRET") 
            or os.getenv("API_SECRET")
        )

        # Validate that credentials exist
        if not all([self.base_url, self.api_key, self.api_secret]):
            raise ValueError(
                f"Missing ERPNext configuration. Checked .env path: {env_path}. "
                "Please ensure ERPNEXT_URL, ERPNEXT_API_KEY, and ERPNEXT_API_SECRET are set."
            )

        self.headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()