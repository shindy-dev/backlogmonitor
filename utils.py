from datetime import datetime

import pytz


class Utils:
    @staticmethod
    def convert_datestringUTC_JST(datestring_utc: str):
        # タイムスタンプをパース
        utc_time = datetime.strptime(datestring_utc, "%Y-%m-%dT%H:%M:%SZ")

        # タイムゾーンをUTCからJSTに変換
        utc_zone = pytz.utc
        jst_zone = pytz.timezone("Asia/Tokyo")

        # UTC時間をタイムゾーンに対応付け
        utc_time = utc_zone.localize(utc_time)
        jst_time = utc_time.astimezone(jst_zone)

        return jst_time.strftime("%Y-%m-%d %H:%M:%S")
