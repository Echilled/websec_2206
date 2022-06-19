from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import hashlib
import time

DRIVER = webdriver.Chrome(ChromeDriverManager().install())
SITE = ["http://randomcolour.com/", "https://www.ledr.com/colours/white.htm", "https://www.utctime.net/"]
INDEX = {}


def hash_indexer():
    with open("WebHash.txt", "r") as rf:
        for line in rf.readlines():
            try:
                url, digest = line.split(",")
                INDEX[url] = digest
            except:
                print("invalid archive")
                continue

def get_web_source():
    for url in SITE:
        DRIVER.get(url)
        time.sleep(1)
        dom = DRIVER.page_source
        print(url, DRIVER.title)
        # print(BeautifulSoup(dom).prettify())
        web_hash_checker(url, hashlib.md5(dom.encode("utf-8")))

    DRIVER.quit()


def web_hash_checker(url, md5):
    digest = md5.hexdigest()
    try:
        print(INDEX[url].strip('\n'), digest)
        if INDEX[url].strip('\n') != digest:
            INDEX[url] = digest
            print("Website does not match previous archive")
        else:
            print("Website match previous archive")
    except:
        INDEX[url] = digest
        print("New webpage archived")


def archive_updater():
    with open("WebHash.txt", "w") as wf:
        print("Updating archive")
        wf.writelines("\n".join(','.join((key,val)) for (key,val) in INDEX.items()))


if __name__ == '__main__':
    hash_indexer()
    # print(INDEX)
    get_web_source()
    archive_updater()