import requests


class GithubInstance:
    def __init__(self, token, host="api.github.com"):
        self.host = host
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}"
        }

    def read(self, uri: str):
        uri = uri.lstrip("/")
        res = requests.get(f"https://{self.host}/{uri}")
        return res.json()

    def list_repos(self, owner):
        return self.read(f"orgs/{owner}/repos")

    def list_git_tree(self, owner, repo,tree_sha):
        return self.read(f"/repos/{owner}/{repo}/git/trees/{tree_sha}")
