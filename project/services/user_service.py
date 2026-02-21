import os
import traceback
from typing import Optional, Dict, Any

import httpx
from pydantic import BaseModel

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


class UserUpsert(BaseModel):
    user_telegram_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
    call_sign: Optional[str] = None
    save_data: Optional[bool] = None


class UserService:
    def __init__(self, api_url: str = API_URL, api_key: Optional[str] = API_KEY):
        self.client = httpx.AsyncClient(
            base_url=api_url.rstrip("/"),
            timeout=httpx.Timeout(10.0, connect=3.0, read=10.0),
            follow_redirects=True,
            http2=True,
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=10),
            headers={
                "Content-Type": "application/json",
            }
        )

        if api_key:
            self.client.headers["x-api-key"] = api_key

    async def upsert_user(self, user_data: UserUpsert) -> Dict[str, Any]:
        try:
            response = await self.client.post("/users/bot", json=user_data.model_dump(mode="json"))
            response.raise_for_status()
            return response.json()

        except Exception:
            print(traceback.format_exc())

    async def close(self):
        await self.client.aclose()
