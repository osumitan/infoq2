from selenium import webdriver

# Byを取得
# data: データ
def get_by(data):
    if data is None:
        return None
    elif data["id"] == "css":
        return ByCss(data["selector"])
    elif data["id"] == "xpath":
        return ByXPath(data["selector"])
    else:
        raise ValueError("illegal by.id: {}", data["id"])

# By
class By:
    # ID
    id = None
    # セレクタ
    selector = None

    # コンストラクタ
    # id: By.ID
    # selector: セレクタ
    def __init__(self, id, selector):
        self.id = id
        self.selector = selector

# CSS用By
class ByCss(By):
    # コンストラクタ
    # selector: セレクタ
    def __init__(self, selector):
        super().__init__(webdriver.common.by.By.CSS_SELECTOR, selector)

# XPath用By
class ByXPath(By):
    # コンストラクタ
    # selector: セレクタ
    def __init__(self, selector):
        super().__init__(webdriver.common.by.By.XPATH, selector)
