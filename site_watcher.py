import filecmp
import hashlib
import os
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import urllib.request

import difflib
from urllib.request import urlopen


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

        # check if directory and previous hash exists
        if os.path.isdir(get_hostname(self._url)) is False:
            os.mkdir(get_hostname(self._url))
            print('First time hash storing')
            with open(get_hostname(self._url) + 'site_256.txt', 'w') as f:
                f.write(sha256_new)
        else:
            with open(get_hostname(self._url)+'site_256_new.txt', 'w') as f:
                f.write(sha256_new)
            return sha256_new


def print_html(URL):
    fp = urllib.request.urlopen(URL)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    print(mystr)


def get_hostname(url):
    if "http://www." in url:
        return url.replace("http://www.","")

    if "https://www." in url:
        return url.replace("https://www.","")


def compare_hash(URL):
    # get latest hash
    SHA256_code = Site_watcher(URL).SHA256_code()

    if os.path.isfile(get_hostname(URL)+'site_256.txt') and os.path.isfile(get_hostname(URL)+'site_256_new.txt'):
            if filecmp.cmp(get_hostname(URL)+'site_256.txt', get_hostname(URL)+'site_256_new.txt'):
                print('Not Updated', SHA256_code)
            else:
                print("site has changed")
                # notify users
                os.remove(get_hostname(URL)+'site_256.txt')
                os.rename(get_hostname(URL)+'site_256_new.txt', get_hostname(URL)+'site_256.txt')


def main():
    URL = 'http://www.beefychilled.tk/'
    compare_hash(URL)
    # # print_html(URL)
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')
    data = soup.find("body").find("script")
    print(data)


if __name__ == '__main__':
    main()
