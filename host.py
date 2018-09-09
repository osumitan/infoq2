import re
import common
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
        self.drv = Driver(self)
        # ホストデータ
        self.data = HostData(self.name)
    
    # ログ
    # str: ログ文字列
    def log(self, str):
        common.log("{} - {}".format(self.data.name, str))
    
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
        # ログ出力
        self.log("ログイン")
    
    # ログアウト
    def logout(self):
        self.drv.click(self.data.login.logout_button)
        self.log("ログアウト")
    
    # 実行
    def run(self):
        self.log("実行開始")
        while True:
            # 次のアンケートを開く
            handle = self.open_next_enquete()
            if handle is None:
                # 全アンケート完了
                break
            try:
                # サイトを生成
                enq = Enquete(self, handle)
                # アンケート実行
                enq.run()
            except(RuntimeWarning) as e:
                self.log(e)
                continue
    
    # 次のアンケートを開く
    # return: サブウィンドウハンドル
    def open_next_enquete(self):
        data = self.data.enquete_list
        # メインウィンドウにスイッチ
        self.drv.switch_main_window(self.main_handle)
        # トップページボタンをクリック
        self.drv.click(data.top_page_button)
        # アンケートリストタブをクリック
        self.drv.click(data.enquete_list_tab)
        # アンケートリンクを取得
        enq_link_list = self.drv.find_element_list(data.enquete_link_list, False)
        # 古いものからチェック
        if not enq_link_list is None:
            for enq_link in reversed(enq_link_list):
                # 未処理なら開く
                enq_id = re.search(r"qid=([0-9a-f]+)", enq_link.get_attribute("onclick")).group(1)
                if not enq_id in self.done_list:
                    # 処理済みに追加
                    self.done_list.append(enq_id)
                    # アンケートリンクをクリック
                    self.drv.click_element(enq_link)
                    # サブウィンドウにスイッチ
                    return self.drv.switch_sub_window(self.main_handle)
        # 全アンケート完了
        self.log("全アンケート終了")
        return None
