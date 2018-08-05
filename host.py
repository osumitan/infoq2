import sys
import io
import re
from abc import ABCMeta
from driver import Driver
from host_data import HostData
from enquete import Enquete

# ホスト
class Host:
    # ドライバ
    drv = None
    # ホストデータ
    data = None
    # メインウィンドウハンドル
    main_handle = None
    # 処理済みアンケートリスト
    done_list = []

    # コンストラクタ
    # name: ホスト名
    def __init__(self, name):
        # ホスト名
        self.name = name
        # ドライバ
        self.drv = Driver()
        # ホストデータ
        self.data = HostData(self.name)
    
    # クローズ
    def close(self):
        self.drv.switch_main_window(self.main_handle)
        self.drv.close_window()
    
    # ログイン
    def login(self):
        data = self.data.login
        # ログインページに移動
        self.drv.go(data.url)
        # メインウィンドウハンドルを保存
        self.main_handle = self.drv.get_current_window_handle()
        # オープナーをクリック
        self.drv.click(data.opener)
        # IDを入力
        self.drv.set_value(data.id_text, data.id)
        # パスワードを入力
        self.drv.set_value(data.password_text, data.password)
        # ログインボタンをクリック
        self.drv.click(data.login_button)
    
    # ログアウト
    def logout(self):
        self.drv.click(self.data.login.logout_button)
    
    # スタート
    def start(self):
        while True:
            # 次のアンケートを開く
            enq = self.open_next_enquete()
            if enq is None:
                break
            enq.close()
    
    # 次のアンケートを開く
    # return: bool
    def open_next_enquete(self):
        data = self.data.enquete_list
        # メインウィンドウにスイッチ
        self.drv.switch_main_window(self.main_handle)
        # トップページボタンをクリック
        self.drv.click(data.top_page_button)
        # アンケートリストタブをクリック
        self.drv.click(data.enquete_list_tab)
        # アンケートリンクを取得
        enq_list = self.drv.find_element_list(data.enquete_link_list)
        # 古いものからチェック
        if not enq_list is None:
            for enq in reversed(enq_list):
                # 未処理なら開く
                enq_id = re.search(r"qid=([0-9a-f]+)", enq.get_attribute("onclick")).group(1)
                if not enq_id in self.done_list:
                    # 処理済みに追加
                    self.done_list.append(enq_id)
                    # アンケートリンクをクリック
                    self.drv.click_element(enq)
                    # サブウィンドウにスイッチ
                    handle = self.drv.switch_sub_window(self.main_handle)
                    # サイトを返す
                    if not handle is None:
                        return Enquete(self.drv, handle)
        # 全アンケート完了
        return None

# ホスト：infoQ
class InfoQHost(Host):
    # コンストラクタ
    def __init__(self):
        super().__init__("infoq")
