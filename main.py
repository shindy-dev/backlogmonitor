import argparse
import datetime
import json
import os
import time

from backlog import BackLog
from settings import Settings
from utils import Utils

# pyinstaller main.py -n backlogmonitor --onefile --clean --strip


def export_projects(api_key: str, space_id: str):
    """プロジェクト情報を出力する"""
    path = os.path.abspath(f"backlog_projects_{space_id}.json")
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(
            BackLog(api_key, space_id).request_projects(),
            f,
            indent=4,
            ensure_ascii=False,
        )
    print(f"{path} にプロジェクト情報を出力しました。")


def export_users(api_key: str, space_id: str, project_id: str):
    """ユーザー情報を出力する"""
    path = os.path.abspath(f"backlog_users_{space_id}_{project_id}.json")
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(
            BackLog(api_key, space_id).request_users(project_id),
            f,
            indent=4,
            ensure_ascii=False,
        )
    print(f"{path} にユーザー情報を出力しました。")


def export_statuses(api_key: str, space_id: str, project_id: str):
    """ステータス情報を出力する"""
    path = os.path.abspath(f"backlog_statuses_{space_id}_{project_id}.json")
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(
            BackLog(api_key, space_id).request_statuses(project_id),
            f,
            indent=4,
            ensure_ascii=False,
        )
    print(f"{path} にステータス情報を出力しました。")


def exportmode(settings: Settings):
    """出力モード"""
    while True:
        print("出力モードを選択してください:")
        print("1: プロジェクト情報")
        print("2: プロジェクトユーザー情報")
        print("3: プロジェクトステータス情報")
        print("q: キャンセル")
        choice = input("選択: ").strip()

        match choice:
            case "1":
                export_projects(settings.api_key, settings.space_id)
            case "2":
                export_users(
                    settings.api_key,
                    settings.space_id,
                    settings.monitor_project_id,
                )
            case "3":
                export_statuses(
                    settings.api_key,
                    settings.space_id,
                    settings.monitor_project_id,
                )
            case "q":
                print("出力モードを終了します。")
                break
            case _:
                print("無効な選択です。もう一度入力してください。")


def monitormode(settings: Settings):
    """監視モード"""
    backlog = BackLog(settings.api_key, settings.space_id)
    projects_info = f" - {settings.monitor_project_id}({[i for i in backlog.request_projects() if i['id'] == int(settings.monitor_project_id)][0]['name']})"
    statuses_info = [
        f" - {i['id']}({i['name']})"
        for i in backlog.request_statuses(settings.monitor_project_id)
        for j in settings.monitor_status_ids
        if i["id"] == int(j)
    ]
    users_info = [
        f" - {i['id']}({i['name']})"
        for i in backlog.request_users(settings.monitor_project_id)
        for j in settings.monitor_user_ids
        if i["id"] == int(j)
    ]
    print("監視モードを開始します。")
    while True:
        try:
            os.system("cls" if os.name == "nt" else "clear")
            print(
                "########################################################################"
            )
            print(
                f"監視中...（Ctrl+Cで終了）最終更新：{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')} "
            )
            print("【プロジェクトID】")
            print(projects_info)

            print("【担当者ID】")
            [print(user) for user in users_info]

            print("【状態ID】")
            [print(status) for status in statuses_info]
            print(
                "########################################################################"
            )

            issues = backlog.request_issues(
                settings.monitor_project_id,
                settings.monitor_user_ids,
                settings.monitor_status_ids,
            )
            if not issues:
                print("\033[36m現在監視対象の課題はありません。\033[0m")
            else:
                print("---------------------------------------------------")
                for issue in issues:
                    print(f"\033[32m課題名：{issue['summary']}")
                    print(f"URL: {backlog.get_url(issue['issueKey'])}")
                    print(
                        f"担当者：{issue['assignee']['name']} 登録者: {issue['createdUser']['name']} 更新日時:{Utils.convert_datestringUTC_JST(issue['created'])}\033[0m"
                    )
                    print("---------------------------------------------------")

            time.sleep(10)  # 5秒間隔で監視（設定により変更可能）
        except KeyboardInterrupt:
            print("監視を終了します。")
            print(
                "########################################################################"
            )
            break


def initialize_settings(settings_path: str):
    """設定ファイルを初期化する"""
    api_key = input("APIキーを入力してください: ")
    space_id = input("スペースIDを入力してください: ")

    export_projects(api_key, space_id)
    project_id = input("プロジェクトIDを入力してください（一覧を確認してください）: ")
    export_users(api_key, space_id, project_id)
    user_ids = input(
        "ユーザーIDをカンマ区切りで入力してください（一覧を確認してください）: "
    )
    export_statuses(api_key, space_id, project_id)
    status_ids = input(
        "ステータスIDをカンマ区切りで入力してください（一覧を確認してください）: "
    )

    settings = Settings(
        settings_path,
        {
            "api_key": api_key,
            "space_id": space_id,
            "monitor_project_id": project_id,
            "monitor_user_ids": user_ids.split(","),
            "monitor_status_ids": status_ids.split(","),
        },
    )
    settings.resave()
    print(f"設定を {settings_path} に保存しました。")


def main():
    defalt_settings_path = "settings.json"
    parser = argparse.ArgumentParser(description="Backlog Watcher CLI")
    parser.add_argument(
        "--settings", type=str, default=defalt_settings_path, help="設定ファイルのパス"
    )
    args = parser.parse_args()

    settings_path = os.path.abspath(args.settings)

    if os.path.exists(settings_path):
        settings = Settings.load(settings_path)
    else:
        print("設定ファイルが見つかりません。初期設定を行います。")
        settings = initialize_settings(settings_path)

    while True:
        print("モードを選択してください:")
        print("1: 監視モード")
        print("2: 出力モード")
        print("q: キャンセル")
        choice = input("選択: ").strip()

        match choice:
            case "1":
                monitormode(settings)
                break
            case "2":
                exportmode(settings)
                break
            case "q":
                print("キャンセルしました。")
                break
            case _:
                print("無効な選択です。もう一度入力してください。")


if __name__ == "__main__":
    main()
