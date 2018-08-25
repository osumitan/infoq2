import enquete_data

# アンケート
class Enquete:
    host = None
    drv = None
    handle = None
    data = None

    # コンストラクタ
    # host: ホスト
    # handle: ウィンドウハンドル
    def __init__(self, host, handle):
        # ホスト
        self.host = host
        # ドライバ
        self.drv = host.drv
        # ウィンドウハンドル
        self.handle = handle
        # アンケートデータ
        self.data = enquete_data.get_enquete_data(host, self.drv.get_url())
    
    # ログ
    # str: ログ文字列
    def log(self, str):
        self.host.log("{} - {}".format(self.data.site.name, str))
    
    # アンケート実行
    def run(self):
        # ログ出力
        self.log("アンケート開始")
        # アンケート回答をループ
        qn = 0
        while(self.continues()):
            # ログ出力
            qn += 1
            self.log("質問{}".format(qn))
            # IFRAMEにスイッチ
            self.drv.switch_frame(self.data.site.iframe)
            # 質問に回答
            self.answer_question()
            # 次へボタンをクリック
            if not self.drv.click(self.data.question.next_button):
                # 次へボタンがクリックできないときは中断
                raise RuntimeWarning("次へボタンがクリックできない")
        else:
            # ログ出力
            self.log("最終質問")
        # 最終ボタンをクリック
        self.drv.click(self.data.question.final_button)
        # ログ出力
        self.log("アンケート終了")
    
    # アンケートを継続するか
    # return: bool
    def continues(self):
        # 最終質問がなければ継続
        return not self.drv.exists(self.data.question.final_text)
    
    # 質問に回答
    def answer_question(self):
        # 特殊質問に回答
        if not self.answer_special_question():
            # 一般質問に回答
            for gen in self.data.question.general:
                if self.drv.click_random(gen):
                    break
    
    # 特殊質問に回答
    # return: 特殊質問に回答したか
    def answer_special_question(self):
        # 特殊質問文があったら回答
        for spdata in self.data.question.special:
            if self.drv.exists(spdata.text):
                return self.drv.click(spdata.answer)
        else:
            return False
