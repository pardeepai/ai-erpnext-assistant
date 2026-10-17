
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class ERPNextAPIError(Exception):
    """Safe, consistent error raised for ERPNext API failures."""


class ERPNextClient:
    def __init__(self):
        self.base_url = (
            os.getenv("ERPNEXT_URL") or os.getenv("ERP_URL")
        )
        self.api_key = (
            os.getenv("ERPNEXT_API_KEY") or os.getenv("API_KEY")
        )
        self.api_secret = (
            os.getenv("ERPNEXT_API_SECRET") or os.getenv("API_SECRET")
        )

        if not all([self.base_url, self.api_key, self.api_secret]):
            raise ValueError(
                "Missing ERPNext configuration. Set the required "
                "URL, API key, and API secret environment variables."
            )

        self.base_url = self.base_url.rstrip("/")

        self.headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10,
            )

            response.raise_for_status()
            return response.json()

        except requests.Timeout as exc:
            logger.warning("ERPNext request timed out: %s", endpoint)
            raise ERPNextAPIError(
                "ERPNext request timed out. Please try again."
            ) from exc

        except requests.ConnectionError as exc:
            logger.warning("ERPNext connection failed: %s", endpoint)
            raise ERPNextAPIError(
                "Unable to connect to ERPNext. Please try again later."
            ) from exc

        except requests.HTTPError as exc:
            status_code = exc.response.status_code

            logger.warning(
                "ERPNext HTTP error: endpoint=%s status=%s",
                endpoint,
                status_code,
            )

            if status_code == 401:
                message = "ERPNext authentication failed."
            elif status_code == 403:
                message = "Permission denied by ERPNext."
            else:
                message = f"ERPNext request failed with status {status_code}."

            raise ERPNextAPIError(message) from exc

        except ValueError as exc:
            # Includes invalid JSON returned by a successful HTTP response.
            logger.warning(
                "Invalid JSON response from ERPNext: %s", endpoint
            )
            raise ERPNextAPIError(
                "ERPNext returned an invalid response."
            ) from exc

        except requests.RequestException as exc:
            logger.warning(
                "ERPNext request failed: endpoint=%s error_type=%s",
                endpoint,
                type(exc).__name__,
            )
            raise ERPNextAPIError(
                "An unexpected ERPNext communication error occurred."
            ) from exc
