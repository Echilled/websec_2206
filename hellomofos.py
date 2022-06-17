
import hashlib
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()

class Site_watcher():
    def __init__(self, url):
        self._url = url

    def md5_code(self):
        # Fake user-agent
        ua = UserAgent()
        # Get source code
        response = requests.get(self._url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        # MD5 hash of source code
        md5_new = hashlib.md5(str(soup).encode()).hexdigest()
        # Save file
        with open('site_md5_new.txt', 'w') as f:
            f.write(md5_new)
        return md5_new


def check_hash(file):
    # A arbitrary (but fixed) buffer size (change accordingly) 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536

    # Initializing the sha256() method
    sha256 = hashlib.sha256()

    # Opening the file provided as the first commandline argument
    with open(file, 'rb') as f:
        while True:
            # reading data = BUF_SIZE from
            # the file and saving it in a
            # variable
            data = f.read(BUF_SIZE)

            # True if eof = 1
            if not data:
                break

            # Passing that data to that sh256 hash
            # function (updating the function with
            # that data)
            sha256.update(data)

    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return sha256.hexdigest()


def compare_hash(file1, file2):
    file1_hash = check_hash(file1)
    file2_hash = check_hash(file2)
    if file1_hash == file2_hash:
        return True
    else:
        return False


def compare_content(file1, file2):
    pass


def main():
    URLs = []

    print(compare_hash('file1.html', 'file2.html'))

main()