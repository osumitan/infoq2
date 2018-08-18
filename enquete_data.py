import glob
import json
import re
import by

# アンケートデータマップ
ENQUETE_DATA_MAP = {}

# アンケートデータを取得
# host: ホスト
# url: URL
# return: アンケートデータ
def get_enquete_data(host, url):
    list = None
    map = ENQUETE_DATA_MAP
    # マップからリストを取得
    if host.data.name in map:
        list = map[host.data.name]
    else:
        # マップにないときはロード
        list = load_enquete_data(host)
        map[host.data.name] = list
    # リストからマッチするサイトを探す
    for data in list:
        if data.matches(url):
            return data
    else:
        # マッチするサイトがない
        raise RuntimeWarning("未知のサイト: host={}, url={}".format(host.data.name, url))

# アンケートデータをロード
# host: ホスト
# return: アンケートデータリスト
def load_enquete_data(host):
    list = []
    # データファイル一覧でループ
    for path in glob.glob("enquete/{}_*.json".format(host.data.name)):
        try:
            list.append(EnqueteData(host.data.name, path))
        except Exception as e:
            host.log("アンケートデータロードエラー: path={}".format(path))
            raise e
    return list

# アンケートデータ
class EnqueteData:
    host_name = None
    site = None
    question = None

    # コンストラクタ
    # host_name: ホスト名
    # path: JSONファイルのパス
    def __init__(self, host_name, path):
        # ホスト名
        self.host_name = host_name
        # JSONをロード
        data = json.load(open(path, "r", encoding="utf-8"))
        # サイト情報
        self.site = EnqueteDataSite(data["site"])
        # 質問情報
        self.question = EnqueteDataQuestion(data["question"])
    
    # マッチ
    # url: URL
    # return: マッチ結果
    def matches(self, url):
        return self.site.matches(url)

# アンケートデータ／サイト情報
class EnqueteDataSite:
    name = None
    description = None
    url_re = None
    iframe = None

    # コンストラクタ
    # data: データ
    def __init__(self, data):
        # サイト名
        self.name = data["name"]
        # サイト説明
        self.description = data["description"]
        # URLの正規表現
        self.url_re = re.compile(data["url_re"])
        # iframe
        self.iframe = by.get_by(data["iframe"]) if "iframe" in data else None
    
    # マッチ
    # url: URL
    # return: マッチ結果
    def matches(self, url):
        return self.url_re.match(url)

# アンケートデータ／質問情報
class EnqueteDataQuestion:
    next_button = None
    final_text = None
    final_button = None
    general = None
    special = None

    # コンストラクタ
    # data: データ
    def __init__(self, data):
        # 次へボタン
        self.next_button = by.get_by(data["next_button"])
        # 最終質問文
        self.final_text = by.get_by(data["final_text"])
        # 最終ボタン
        self.final_button = by.get_by(data["final_button"])
        # 一般質問
        self.general = []
        for general_data in data["general"]:
            self.general.append(by.get_by(general_data))
        # 特殊質問
        self.special = []
        if "special" in data:
            for special_data in data["special"]:
                self.special.append(EnqueteDataQuestionSpecial(special_data))

# アンケートデータ／質問情報／特殊質問
class EnqueteDataQuestionSpecial:
    text = None
    answer = None

    # コンストラクタ
    # data: データ
    def __init__(self, data):
        # 質問文
        self.text = by.get_by(data["text"])
        # 回答選択肢
        self.answer = by.get_by(data["answer"])