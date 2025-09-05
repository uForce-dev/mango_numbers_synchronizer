import hashlib
import json
import requests
import logging
from typing import Optional
from config import settings
from models import MangoApiResponse

logger = logging.getLogger(__name__)


class MangoOfficeClient:
    def __init__(self):
        self.api_key = settings.mango_api_key
        self.salt = settings.mango_salt
        self.api_url = "https://app.mango-office.ru/vpbx/incominglines"

    def _generate_signature(self, json_data: str) -> str:
        sign_str = self.api_key + json_data + self.salt
        return hashlib.sha256(sign_str.encode("utf-8")).hexdigest()

    def get_phone_numbers(self) -> Optional[MangoApiResponse]:
        try:
            payload = {}
            json_data = json.dumps(payload, separators=(",", ":"))
            sign = self._generate_signature(json_data)

            params = {"vpbx_api_key": self.api_key, "sign": sign, "json": json_data}

            logger.info(f"Request to Mango Office API: {self.api_url}")

            response = requests.post(
                self.api_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )

            logger.info(f"API response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Fetched data: {len(data.get('lines', []))} numbers")
                return MangoApiResponse(**data)
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
