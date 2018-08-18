from datetime import datetime

# ログ
# str: ログ文字列
def log(str):
    print("[{}] {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str))