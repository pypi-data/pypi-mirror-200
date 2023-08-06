import logging
from enum import Enum
from typing import Dict

import requests


class AccountStatusEnum(Enum):
    commissioned = "commissioned"
    pending = "pending"
    decommissioned = "decommissioned"
    decommissioning = "decommissioning"  # Update Status to "decommissioning" to trigger cloud sso disconnect


class FinTool:
    def __init__(self, endpoint: str, key):
        self.session = requests.Session()
        self.session.headers.setdefault("X-Auth-Key", key)
        self.endpoint = endpoint.strip("/")

    def request(self, method: str, path: str, json_payload=None):
        url = self.endpoint + path

        request_param = {
            "method": method.lower(),
            "url": url
        }
        if json_payload:
            request_param.setdefault("json", json_payload)
        res = self.session.request(**request_param, verify=False)
        if res.status_code / 100 == 2:
            return res.json()
        if res.status_code / 100 == 5:
            logging.error(res.text)

    def list_accounts(self):
        return self.request("get", "/accounts")

    def get_account(self, account_id):
        return self.request("get", f"/accounts/{account_id}")

    def update_account_info(self, account_id, change_info):
        return self.request("put", f"/accounts/{account_id}", json_payload=change_info)

    def update_account_status(self, account_id, status: AccountStatusEnum = None,
                              tags: Dict[str, str | dict] = None):
        account_info = {}
        if status:
            account_info['status'] = status.value
        if tags:
            account_info['tags'] = tags
        return self.update_account_info(account_id, account_info)

    def __filter_alicloud_active_accounts(self, provider: str = "alicloud"):
        accounts_filtered = []
        accounts = self.list_accounts()["accounts"]
        for x in accounts:
            if x["provider"] != provider:
                continue
            if x["status"] != "commissioned":
                continue
            if x["type"] != "real":
                continue
            accounts_filtered.append(x)
        return accounts_filtered
