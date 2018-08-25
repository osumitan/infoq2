import time
import random
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# ドライバ
class Driver:
    # リトライ間隔（秒）
    RETRY_INTERVAL = 2
    # リトライ回数
    RETRY_LIMIT = 30
    
    __drv = None
    host = None

    # コンストラクタ
    # host: ホスト
    def __init__(self, host):
        # ドライバ初期化
        self.__drv = webdriver.Chrome("../lib/chromedriver.exe")
        self.__drv.set_window_size(1152, 768)
        self.__drv.set_window_position(376, 44)
        self.__drv.set_page_load_timeout(20)
        # ホスト
        self.host = host
    
    # ログ
    # str: ログ文字列
    def log(self, str):
        self.host.log("{} - {}".format("driver", str))
    
    # ウィンドウを閉じる
    def close_window(self):
        self.__drv.close()
    
    # 現在のウィンドウハンドルを取得
    # return: ウィンドウハンドル
    def get_current_window_handle(self):
        return self.__drv.current_window_handle
    
    # ウィンドウハンドルリストを取得
    # return: ウィンドウハンドルリスト
    def get_window_handle_list(self):
        return self.__drv.window_handles
    
    # ウィンドウをスイッチ
    # handle: ウィンドウハンドル
    def switch_window(self, handle):
        self.__drv.switch_to.window(handle)
    
    # メインウィンドウにスイッチ
    # main_handle: メインウィンドウハンドル
    def switch_main_window(self, main_handle):
        # メインウィンドウ以外を閉じる
        for handle in self.get_window_handle_list():
            if handle != main_handle:
                self.switch_window(handle)
                self.close_window()
        # メインウィンドウにスイッチ
        self.switch_window(main_handle)
    
    # サブウィンドウにスイッチ
    # main_handle: メインウィンドウハンドル
    # wait: 見つかるまで待つか
    # return: サブウィンドウハンドル
    def switch_sub_window(self, main_handle, wait = True):
        retry = 0 if wait else self.RETRY_LIMIT
        while True:
            # メイン以外のウィンドウがあったらスイッチ
            for handle in self.get_window_handle_list():
                if handle != main_handle:
                    self.switch_window(handle)
                    return handle
            else:
                if retry < self.RETRY_LIMIT:
                    retry += 1
                    time.sleep(self.RETRY_INTERVAL)
                else:
                    break
        else:
            if wait:
                self.log("timeout - switch_sub_window")
            return None
    
    # フレームにスイッチ
    # by: By
    def switch_frame(self, by):
        if self.exists(by):
            self.__drv.switch_to.frame(self.find_element(by))
    
    # 現在のURLを取得
    # return: URL
    def get_url(self):
        return self.__drv.current_url
    
    # ページ移動
    # url: URL
    def go(self, url):
        self.__drv.get(url)
    
    # エレメントを検索
    # by: By
    # wait: 見つかるまで待つか
    # return: エレメント
    def find_element(self, by, wait = True):
        retry = 0 if wait else self.RETRY_LIMIT
        while True:
            elm = self.__drv.find_element(by.id, by.selector)
            if not elm is None:
                return elm
            elif retry < self.RETRY_LIMIT:
                retry += 1
                time.sleep(self.RETRY_INTERVAL)
            else:
                if wait:
                    self.log("timeout - find_element")
                return None
    
    # エレメントリストを検索
    # by: By
    # wait: 見つかるまで待つか
    # return: エレメントリスト
    def find_element_list(self, by, wait = True):
        retry = 0 if wait else self.RETRY_LIMIT
        while True:
            elm_list = self.__drv.find_elements(by.id, by.selector)
            if not elm_list is None and len(elm_list) >= 1:
                return elm_list
            elif retry < self.RETRY_LIMIT:
                retry += 1
                time.sleep(self.RETRY_INTERVAL)
            else:
                if wait:
                    self.log("timeout - find_element_list")
                return []
    
    # エレメントが存在するか
    # by: By
    # wait: 見つかるまで待つか
    # return: bool
    def exists(self, by, wait = False):
        return len(self.find_element_list(by, wait)) >= 1 if not by is None else False
    
    # クリック
    # by: By
    # return: クリックしたか
    def click(self, by):
        if self.exists(by):
            retry = 0
            while True:
                try:
                    return self.click_element(self.find_element(by))
                except exceptions.StaleElementReferenceException as e:
                    # リトライ
                    if retry < self.RETRY_LIMIT:
                        retry += 1
                        time.sleep(self.RETRY_INTERVAL)
                    else:
                        self.log("timeout - click")
                        raise e
        else:
            return False
    
    # エレメントをクリック
    # elm: エレメント
    # return: クリックしたか
    def click_element(self, elm):
        # 有効チェック
        if not elm.is_enabled():
            return False
        # エラー発生時はリトライ
        retry = 0
        while True:
            try:
                # マウスオーバー
                ac = ActionChains(self.__drv)
                ac.move_to_element(elm)
                ac.perform()
                # クリック
                elm.click()
                return True
            except exceptions.StaleElementReferenceException as e:
                # 呼出元でリトライするためraise（find_elementをやり直す）
                raise e
            except exceptions.WebDriverException as e:
                # リトライ
                if retry < self.RETRY_LIMIT:
                    retry += 1
                    time.sleep(self.RETRY_INTERVAL)
                else:
                    self.log("timeout - click_element")
                    raise e
    
    # ランダムクリック
    # by: By
    # return: クリックしたか
    def click_random(self, by):
        # エレメントを検索
        if self.exists(by):
            elm_list = self.find_element_list(by)
            if not elm_list is None and len(elm_list) >= 1:
                # ランダムにクリック（3件以上あるときは最後を選ばせない）
                limit = len(elm_list) - 1 if len(elm_list) >= 3 else len(elm_list)
                return self.click_element(elm_list[random.randrange(limit)])
            else:
                return False
    
    # value設定
    # by: By
    # value: value
    def set_value(self, by, value):
        if self.exists(by):
            self.find_element(by).send_keys(value)
