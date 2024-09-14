from functools import reduce
import json
from typing import Any, Dict, List
import aiohttp
import asyncio
from bs4 import BeautifulSoup

from portals.shared_logic import RentPortal


class ClickPay(RentPortal):
    def __init__(self, user_name: str, user_password: str) -> None:
        self.user_name = user_name
        self.user_password = user_password
        self.headers = {
            "accept": "*/*",
            "content-type": "text/plain; charset=UTF-8",
            "origin": "https://clickpay.com",
            "referer": "https://clickpay.com/",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        self.base_url = "https://clickpay.com/MobileService/Service.asmx"
        self.session = None


    async def start_session(self) -> None:
        await self._get_cookie()
        await self._get_anti_forgery_token()

    async def get_data(self) -> Dict[str, str]:
        results = await asyncio.gather(
            self._get_user_context(), self._get_data_allow_impersonation()
        )
        return reduce(lambda acc, d: acc.update(d) or acc, results, {})

    async def _get_cookie(self) -> None:
        url = f"{self.base_url}/prepare_login"
        payload = {"prepare": "login"}

        async with self.session.post(
            url, headers=self.headers, data=json.dumps(payload)
        ) as response:
            response.raise_for_status()
            cookies = self.session.cookie_jar.filter_cookies(url)
            secure_session_id = cookies.get("__Secure-SessionId")
            if not secure_session_id:
                raise ValueError("No Secure-SessionId found in cookies.")
            self.headers["Cookie"] = f"__Secure-SessionId={secure_session_id.value}"

    async def _get_anti_forgery_token(self):
        payload = {
            "username": self.user_name,
            "password": self.user_password,
            "validateUsername": True,
        }

        async with self.session.post(
            f"{self.base_url}/login", headers=self.headers, data=json.dumps(payload)
        ) as response:
            response.raise_for_status()
            redirect_url = "https://clickpay.com/app#PayNow"
            async with self.session.get(
                redirect_url, headers=self.headers
            ) as redirect_response:
                redirect_response.raise_for_status()
                soup = BeautifulSoup(await redirect_response.text(), "html.parser")
                anti_forgery_token = soup.find(
                    "input", {"name": "ctl00$antiForgeryToken"}
                )["value"]
                if not anti_forgery_token:
                    raise ValueError("antiforgerytoken not found")
                self.headers["antiforgerytoken"] = anti_forgery_token

    async def _get_user_context(self) -> Dict[str, Any]:
        payload = "NovelPayApp"

        async with self.session.post(
            f"{self.base_url}/getUserContextJSON", headers=self.headers, data=payload
        ) as response:
            response.raise_for_status()
            data = await response.json()
            if "Result" not in data:
                raise ValueError("Cannot get the data. Validate login details")
            user_data = data["Result"]["user"]
            return {"email": user_data["Email"], "phone": user_data["Cellphone"]}

    async def _get_data_allow_impersonation(self) -> List[Dict[str, Any]]:
        endpoint = "/get_data_allow_impersonation_json"
        payload = {
            "RequestType": "get_user_paynow_desktop",
            "FilterByGroupLabel": "1",
            "GroupLabel": "",
        }

        async with self.session.post(
            f"{self.base_url}{endpoint}", headers=self.headers, data=json.dumps(payload)
        ) as response:
            response.raise_for_status()
            data = await response.json()
            if "Result" not in data:
                raise ValueError("Cannot get the data. Validate login details")
            unit = data["Result"]["Unit"]["Unit"]
            management_company = unit["SiteName"]
            address = f"{unit['StreetNumber']} {unit['StreetName']} {unit['StreetTypeName']}, {unit['City']} - {unit['State']} ({unit['Zip']})"
            return {"management_company": management_company, "address": address}
