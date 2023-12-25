from typing import Dict, List, Optional

import aiohttp


class SmsClient:
    def __init__(self, login: str, password: str, method: Optional[str]):
        self.login = login
        self.password = password

        self.method = method or 'POST'
        self.http_headers: Dict[str, str] = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.action: List = []

        self.multipost = False
        self.post_data: Dict = {}

        self.url = 'https://a2p-sms-https.beeline.ru/proto/http/rest'

    def set_action(self, action):
        if not self.multipost:
            self.action = []
        self.action.append(action)

    async def send_request(self):
        post_fields = {
            'user': self.login,
            'pass': self.password,

        }
        if not self.multipost:
            post_fields_action = self.action[0].form_post_fields()
        else:
            post_fields_action = {'data': [action.form_post_fields() for action in self.action]}

        post_fields.update(post_fields_action)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=post_fields, headers=self.http_headers) as response:
                return await response.json()

    def is_multipost(self):
        return self.multipost

    def build_headers(self):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
        headers.update(self.http_headers)
        return headers

    def add_header(self, header_name: str, header_value: str):
        self.http_headers[header_name] = header_value  # type: ignore

    def start_multipost(self):
        self.multipost = True
