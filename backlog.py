"""
https://developer.nulab.com/ja/docs/backlog/
"""

import requests
from PIL import Image


class BackLog:
    """BackLog APIに基づくクラス"""

    def __init__(self, api_key: str, space_id: str):
        self.api_key = api_key
        self.space_id = space_id

    def _get_api_url(self, *function_name):
        return f"https://{self.space_id}.backlog.jp/api/v2/{'/'.join(function_name)}"

    def get_url(self, issueKey):
        return f"https://{self.space_id}.backlog.jp/view/{issueKey}"

    @staticmethod
    def _is_success_request(status_code: int) -> bool:
        """リクエスト結果"""
        match status_code:
            case 200:
                return True
            case 403:
                raise Exception(f"アクセス拒否：{status_code}")
            case _:
                raise Exception(f"エラー：{status_code}")

    def request_projects(self) -> list:
        """プロジェクト取得"""
        projects = []

        params = {
            "apiKey": self.api_key,
        }

        # GETリクエストを送信
        response = requests.get(self._get_api_url("projects"), params=params)
        # 結果の表示
        if BackLog._is_success_request(response.status_code):
            projects = response.json()

        return projects

    def request_users(self, project_id: str) -> list:
        """プロジェクトユーザー取得"""
        users = []

        params = {
            "apiKey": self.api_key,
        }

        # GETリクエストを送信
        response = requests.get(
            self._get_api_url("projects", project_id, "users"), params=params
        )
        # 結果の表示
        if BackLog._is_success_request(response.status_code):
            users = response.json()

        return users

    def request_statuses(self, project_id: str) -> list:
        """プロジェクトユーザー取得"""
        users = []

        params = {
            "apiKey": self.api_key,
        }

        # GETリクエストを送信
        response = requests.get(
            self._get_api_url("projects", project_id, "statuses"), params=params
        )
        # 結果の表示
        if BackLog._is_success_request(response.status_code):
            users = response.json()

        return users

    def request_issues(
        self, project_id: str, assigneeId: str = "", statusId: str = ""
    ) -> list:
        """課題取得"""
        params = {"apiKey": self.api_key, "projectId[]": project_id}
        if assigneeId:
            params["assigneeId[]"] = assigneeId
        if statusId:
            params["statusId[]"] = statusId
        # 件数取得
        issues_count: int = requests.get(
            self._get_api_url("issues", "count"), params=params
        ).json()["count"]

        # 課題取得
        issues = []
        for i in range(0, issues_count, 100):
            params = {
                "apiKey": self.api_key,
                "projectId[]": project_id,
                "count": 100,  # 最大100
                "offset": i,
            }
            if assigneeId:
                params["assigneeId[]"] = assigneeId
            if statusId:
                params["statusId[]"] = statusId
            # GETリクエストを送信
            response = requests.get(self._get_api_url("issues"), params=params)
            # 結果の表示
            if BackLog._is_success_request(response.status_code):
                issues.extend(response.json())

        return issues

    def request_spaceIcon(self, project_id: str) -> Image:
        """image取得"""

        # 課題取得
        image = None
        params = {
            "apiKey": self.api_key,
            "projectId[]": project_id,
        }

        # GETリクエストを送信
        with requests.get(
            self._get_api_url("space", "image"), params=params, stream=True
        ) as response:
            # 結果の表示
            if BackLog._is_success_request(response.status_code):
                image = Image.open(response.raw)

        return image

    def request_test(self, project_id: str):
        data = None

        # 課題取得
        params = {
            "apiKey": self.api_key,
            "projectId[]": project_id,
        }

        # GETリクエストを送信
        response = requests.get(
            self._get_api_url("users/1074274068", "stars"), params=params
        )

        # 結果の表示
        if BackLog._is_success_request(response.status_code):
            data = response.json()

        return data
