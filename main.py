import sys
import io
from host import InfoQHost

# メイン
def main():
    h = InfoQHost()
    h.login()
    h.start()
    h.logout()
    h.close()

# メイン
main()
