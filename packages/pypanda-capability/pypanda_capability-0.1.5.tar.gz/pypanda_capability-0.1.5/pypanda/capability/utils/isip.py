import base64
import datetime
import hmac
import json
import logging
import random
import string
from json import JSONDecodeError
from typing import TypedDict

import requests

logger = logging.getLogger("isip_client")

READONLY_POLICY_DOCUMENT = {
    "Version": "1",
    "Statement": [
        {
            "Action": [
                "*:Describe*",
                "*:List*",
                "*:Get*",
                "*:BatchGet*",
                "*:Query*",
                "*:BatchQuery*",
                "actiontrail:LookupEvents",
                "actiontrail:Check*",
                "dm:Desc*",
                "dm:SenderStatistics*",
                "ram:GenerateCredentialReport",
                "cloudsso:Check*",
                "notifications:Read*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
READONLY_POLICY_NAME = "DeskTaskReader"
READONLY_ROLE_NAME = "GetAlicloudResource"


class HmacSigner:
    def __init__(self, key: str):
        self.hmac_salt = key.encode()
        self.hash = 'sha256'

    def sign_bytes(self, _bytes: bytes):
        return hmac.digest(self.hmac_salt, _bytes, self.hash).hex()

    def sign_payload(self, payload: dict):
        payload_bytes = json.dumps(payload, ensure_ascii=False).encode()
        payload_str_b64_encoded = base64.b64encode(payload_bytes)
        return payload_str_b64_encoded.decode(), self.sign_bytes(payload_str_b64_encoded)

    def unload(self, b64_payload: str, b64_payload_sign: str) -> dict | None:
        digest = self.sign_bytes(b64_payload.encode())
        if hmac.compare_digest(digest, b64_payload_sign):
            payload = base64.b64decode(b64_payload)
            return json.loads(payload)
        else:
            return None


class AssumeRoleSecrets(TypedDict):
    access_key: str
    secret_key: str
    security_token: str


class AssumeRole(TypedDict):
    role_name: str
    policy_name: str
    secrets: AssumeRoleSecrets


class IsipClient:
    def __init__(self, endpoint, admin, hmac_key):
        self.endpoint = endpoint
        self.admin = admin
        self.signer = HmacSigner(key=hmac_key)

    def get_login_request(self):
        payload = {"email": self.admin}
        if payload.get("timestamp", None) is None:
            payload["timestamp"] = int(datetime.datetime.now().timestamp())
        if payload.get("nonce", None) is None:
            payload["nonce"] = "".join(
                [
                    random.choice(string.digits + string.ascii_lowercase)
                    for _ in range(8)
                ]
            )

        return self.signer.sign_payload(payload)

    def get_session(self):
        request, request_sign = self.get_login_request()
        url = f"{self.endpoint}/api/v1/core/session/login?payload={request}&sign={request_sign}"
        data = requests.get(url).json()
        return data["payload"]["session_id"]

    @property
    def headers(self):
        return {"X-SESSION-ID": self.get_session()}

    def request(self, method, path, *args, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self.headers)
        res = requests.request(
            method, f"{self.endpoint}/{path}", headers=headers, *args, **kwargs
        )
        try:

            assert res.status_code // 100 == 2
            res_json = res.json()
            return res_json["payload"]
        except (JSONDecodeError, KeyError, AssertionError):
            return {"error": res.text, "status": res.status_code}

    def read(self, path):
        return self.request("GET", path)

    def get_alicloud_credential(
            self, account_id, role_name, policy_name, policy_document
    ):
        data = {
            "account_id": account_id,
            "role_name": role_name,
            "policy_name": policy_name,
            "policy_document": policy_document,
        }
        return self.request("POST", "api/v1/alicloud/getAccountSecrets", json=data)

    def get_alicloud_readonly_role(self, account_id) -> AssumeRole:
        """
        :param account_id:
        :return: AssumeRole
        """
        credential = self.get_alicloud_credential(
            account_id, READONLY_ROLE_NAME, READONLY_POLICY_NAME, READONLY_POLICY_DOCUMENT
        )
        if credential:
            return AssumeRole(**credential)
