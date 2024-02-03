from urllib import parse
import requests
from typing import Dict, Optional
import aiohttp
import ssl
import certifi
from backend.core.config.env import env

from .exceptions import InvalidAuthorizationCode, InvalidToken


class OAuthClient:
    def __init__(
        self,
        client_id,
        client_secret_id,
        redirect_uri,
        authentication_uri,
        resource_uri,
        verify_uri,
    ):
        self._client_id = client_id
        self._client_secret_id = client_secret_id
        self._redirect_uri = redirect_uri
        self._authentication_uri = authentication_uri
        self._resource_uri = resource_uri
        self._verify_uri = verify_uri
        self._header_name = "Authorization"
        self._header_type = "Bearer"

    def _get_connector_for_ssl(self) -> aiohttp.TCPConnector:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        return aiohttp.TCPConnector(ssl=ssl_context)

    async def _request_get_to(self, url, headers=None) -> Optional[Dict]:
        conn = self._get_connector_for_ssl()
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(url, headers=headers) as resp:
                return None if resp.status != 200 else await resp.json()

    async def _request_post_to(self, url, payload=None) -> Optional[dict]:
        conn = self._get_connector_for_ssl()
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.post(url, data=payload) as resp:
                return None if resp.status != 200 else await resp.json()

    def get_oauth_login_url(self, state: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "state": state,
        }
        query_param = parse.urlencode(params, doseq=True)

        return f"{self._authentication_uri}/authorize?{query_param}"

    def get_token_from_kakao(self, code: str, state: str|None) -> str:
        url = "https://kauth.kakao.com/oauth/token"
        cid = env.KAKAO_CLIENT_ID
        cs = env.KAKAO_CLIENT_SECRET_ID
        payload = {
            "client_id": cid,
            "client_secret": cs,
            "grant_type": "authorization_code",
            "code": code,
            # "state": '',
        }
        res = requests.post(url, data=payload,headers={'Content-Type': 'application/x-www-form-urlencoded'})
        t = res.text
        a = res.json()
        ac = a.get('access_token')

        return ac

    def get_tokens(self, code: str, state: str) -> dict:
        tokens = self._request_post_to(
            url=f"{self._authentication_uri}/token",
            payload={
                "client_id": self._client_id,
                "client_secret": self._client_secret_id,
                "grant_type": "authorization_code",
                "code": code,
                # "state": state,
            },
        )
        # if tokens is None:
        #     raise InvalidAuthorizationCode

        # if tokens.get("access_token") is None or tokens.get("refresh_token") is None:
        #     raise InvalidAuthorizationCode

        return tokens

    async def refresh_access_token(self, refresh_token: str) -> Dict:
        tokens = await self._request_post_to(
            url=f"{self._authentication_uri}/token",
            payload={
                "client_id": self._client_id,
                "client_secret": self._client_secret_id,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )
        if tokens is None:
            raise InvalidToken
        return tokens

    def get_user_info(self, access_token: str) -> dict:
        headers = {self._header_name: f"{self._header_type} {access_token}"}
        url=self._resource_uri
        res = requests.get(url,headers=headers)
        print(f'res;{res}')
        # self._request_get_to(url=self._resource_uri, headers=headers)
        # if user_info is None:
        #     raise InvalidToken
        # return user_info
        return res.json()

    async def is_authenticated(self, access_token: str) -> bool:
        headers = {self._header_name: f"{self._header_type} {access_token}"}
        res = await self._request_get_to(
            url=self._verify_uri,
            headers=headers,
        )
        return res is not None
