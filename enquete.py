import sys
import io
from abc import ABCMeta

# アンケート
class Enquete:
    # ドライバ
    drv = None
    # ウィンドウハンドル
    handle = None

    # コンストラクタ
    # drv: ドライバ
    # handle: ウィンドウハンドル
    def __init__(self, drv, handle):
        # ドライバ
        self.drv = drv
        # ウィンドウハンドル
        self.handle = handle
    
    # クローズ
    def close(self):
        self.drv.switch_window(self.handle)
        self.drv.close_window()
