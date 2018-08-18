from host import Host

# メイン
def main():
    h = Host("infoq")
    h.login()
    h.run()
    h.logout()
    h.close()

# メイン
main()
