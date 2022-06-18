import filecmp
import hashlib
import os
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

        # MD5 hash of source code
        sha256_new = hashlib.sha256(str(soup).encode()).hexdigest()
        # Save file
        with open('site_256_new.txt', 'w') as f:
            f.write(sha256_new)
        return sha256_new


# def compare_hash(file1, file2):
#     file1_hash = check_hash(file1)
#     file2_hash = check_hash(file2)
#     if file1_hash == file2_hash:
#         return True
#     else:
#         return False


def main():
    URLs = []
    URL = 'http://www.beefychilled.tk/'
    # get latest hash
    SHA256_code = Site_watcher(URL).SHA256_code()
    if os.path.isfile('site_256.txt'):
            if filecmp.cmp('site_256.txt', 'site_256_new.txt'):
                    print('Not Updated', SHA256_code)
            else:
                print("site has changed")


if __name__ == '__main__':
    main()
    