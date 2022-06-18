import filecmp
import hashlib
import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


class Site_watcher():
    def __init__(self, url):
        self._url = url

    def SHA256_code(self):
        # Fake user-agent
        ua = UserAgent()
        # Get source code
        response = requests.get(self._url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(response.text, "html.parser")

        # SHA256 hash of source code
        sha256_new = hashlib.sha256(str(soup).encode()).hexdigest()

        # check if directory exists
        if os.path.isdir(get_hostname(self._url)) is False:
            os.mkdir(get_hostname(self._url))
            print('First time hash storing')
            with open(get_hostname(self._url) + 'site_256.txt', 'w') as f:
                f.write(sha256_new)
        else:
            with open(get_hostname(self._url)+'site_256_new.txt', 'w') as f:
                f.write(sha256_new)
            return sha256_new


def get_hostname(url):
    if "http://www." in url:
        return url.replace("http://www.","")

    if "https://www." in url:
        return url.replace("https://www.","")


def compare_hash(URL):
    # get latest hash
    SHA256_code = Site_watcher(URL).SHA256_code()

    if os.path.isfile(get_hostname(URL)+'site_256.txt') and os.path.isfile(get_hostname(URL)+'site_256_new.txt'):
            if filecmp.cmp('site_256.txt', 'site_256.txt'):
                print('Not Updated', SHA256_code)
            else:
                print("site has changed")


def main():
    URL = 'http://www.google.com/'
    compare_hash(URL)


if __name__ == '__main__':
    main()
