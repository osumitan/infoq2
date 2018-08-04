import sys
import io
from abc import ABCMeta, abstractmethod
import json
from selenium import webdriver
import by

# ログイン情報
class LoginInfo:
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
        self.url = data["url"]
        self.opener = by.get_by(data["opener"])
        self.id = data["id"]
        self.id_text = by.get_by(data["id_text"])
        self.password = data["password"]
        self.password_text = by.get_by(data["password_text"])
        self.login_button = by.get_by(data["login_button"])
        self.logout_button = by.get_by(data["logout_button"])

# ホスト
class Host:
    # ドライバ
    driver = None
    # ホスト名
    name = None
    # ログイン情報
    login_info = None

    # コンストラクタ
    # name: ホスト名
    def __init__(self, name):
        # ホスト名
        self.name = name
        # ドライバ初期化
        self.driver = webdriver.Chrome("../lib/chromedriver.exe")
        self.driver.set_window_size(1440, 768)
        self.driver.set_window_position(128, 64)
        self.driver.set_page_load_timeout(20)
        # ホスト設定ロード
        data = json.load(open("host/{}.json".format(self.name), "r"))
        self.login_info = LoginInfo(data["login_info"])
    
    # クローズ
    def close(self):
        self.driver.close()
    
    # ページ移動
    # url: URL
    def go(self, url):
        self.driver.get(url)
    
    # エレメント検索
    # by: By
    # return: エレメント
    def find_element(self, by):
        return self.driver.find_element(by.id, by.selector) if not by is None else None
    
    # エレメントが存在するか
    # by: By
    # return: bool
    def exists(self, by):
        return not self.find_element(by) is None if not by is None else False
    
    # クリック
    # by: By
    def click(self, by):
        if self.exists(by):
            self.find_element(by).click()
    
    # value設定
    # by: By
    # value: value
    def set_value(self, by, value):
        if self.exists(by):
            self.find_element(by).send_keys(value)
    
    # ログイン
    def login(self):
        l = self.login_info
        self.go(l.url)
        self.click(l.opener)
        self.set_value(l.id_text, l.id)
        self.set_value(l.password_text, l.password)
        self.click(l.login_button)
    
    # ログアウト
    def logout(self):
        self.click(self.login_info.logout_button)

# ホスト：infoQ
class InfoQHost(Host):
    # コンストラクタ
    def __init__(self):
        super().__init__("infoq")
