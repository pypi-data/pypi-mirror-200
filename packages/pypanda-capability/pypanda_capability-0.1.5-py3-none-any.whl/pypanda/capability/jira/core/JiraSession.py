import requests
import urllib3.exceptions
from pypanda.core.decorator import retry_on_exception
from pypanda.core.exception import PyPleaseRetryError, PyUnHandlerError
from requests.auth import HTTPBasicAuth


class JiraSession:
    def __init__(self, server: str, username, password):
        self.server = f"{server}"
        self.username = username
        self.password = password
        self.session = self.get_authed_session(username, password)

    @staticmethod
    def get_authed_session(username, password):
        session = requests.session()
        session.auth = HTTPBasicAuth(username, password)
        return session

    @retry_on_exception([PyPleaseRetryError], [3, 5, 8, 10, 10])
    def request(self, method, url, *args, **kwargs):
        error = None
        try:
            response = self.session.request(method, url, *args, **kwargs, timeout=20)
            state = response.status_code // 100
            if state in [2, 3]:
                return response
            elif state == 5:
                error = PyPleaseRetryError(f"Retry for Jira Server {response.status_code}: {response.text}")
            else:
                error = PyUnHandlerError(f"UnHandler Error for Jira Server {response.status_code} {response.text}")
        except (requests.exceptions.Timeout, urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.HTTPError, requests.exceptions.ReadTimeout, requests.RequestException):
            error = PyPleaseRetryError(f"Retry for Jira Server Read Timeout")
        if error:
            raise error

    def get_current_user(self):
        return self.request("get", self.server + "/rest/auth/1/session").json()

    def refresh_token(self, description):
        res = self.request("post", self.server + "/rest/de.resolution.apitokenauth/latest/user/token",
                           json={"tokenDescription": description})
        return res.json()
