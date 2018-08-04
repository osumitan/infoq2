import sys
import io
from selenium import webdriver
import host

# メイン
def main():
    h = host.InfoQHost()
    h.login()
    h.logout()
    h.close()

# メイン
main()
