import sys
import io
from abc import ABCMeta
import json
import by

# ホストデータ
class HostData:
    name = None
    login = None
    enquete_list = None

    # コンストラクタ
    # name: ホスト名
    def __init__(self, name):
        # ホスト名
        self.name = name
        # JSONロード
        data = json.load(open("host/{}.json".format(self.name), "r"))
        # ログイン情報
        self.login = HostDataLogin(data["login"])
        # アンケートリスト情報
        self.enquete_list = HostDataEnqueteList(data["enquete_list"])        

# ホストデータ／ログイン情報
class HostDataLogin:
    url = None
    opener = None
    id = None
    id_text = None
    password = None
    password_text = None
    login_button = None
    logout_button = None

    # コンストラクタ
    # data: データ
    def __init__(self, data):
        # URL
        self.url = data["url"]
        # オープナー
        self.opener = by.get_by(data["opener"])
        # ID値
        self.id = data["id"]
        # IDテキスト
        self.id_text = by.get_by(data["id_text"])
        # パスワード値
        self.password = data["password"]
        # パスワードテキスト
        self.password_text = by.get_by(data["password_text"])
        # ログインボタン
        self.login_button = by.get_by(data["login_button"])
        # ログアウトボタン
        self.logout_button = by.get_by(data["logout_button"])

# ホストデータ／アンケートリスト情報
class HostDataEnqueteList:
    top_page_button = None
    enquete_list_tab = None
    enquete_link_list = None

    # コンストラクタ
    # data: データ
    def __init__(self, data):
        # トップページボタン
        self.top_page_button = by.get_by(data["top_page_button"])
        # アンケートリストタブ
        self.enquete_list_tab = by.get_by(data["enquete_list_tab"])
        # アンケートリンクリスト
        self.enquete_link_list = by.get_by(data["enquete_link_list"])
