import difflib
import os
import urllib
from difflib import Differ
from pprint import pprint
from selenium import webdriver
from lxml.html.diff import htmldiff
from bs4 import BeautifulSoup
import hashlib
import time
import datetime
import json
import crawler
import re
import urllib.request

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


DRIVER = webdriver.Chrome("chromedriver.exe")
SITE = ["https://www.ledr.com/colours/white.htm", "http://randomcolour.com/"]
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
        ad_blocker()
        time.sleep(1)
        dom = DRIVER.page_source
        print(url, DRIVER.title)
        page_indexer(DRIVER.page_source, DRIVER.title)
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
            page_checker(DRIVER.title)
        else:
            print("Website match previous archive")
            os.remove(DRIVER.title + "_new.html")


    except:
        INDEX[url] = digest
        print("New webpage archived")


def archive_updater():
    with open("WebHash.txt", "w+") as wf:
        print("Updating archive")
        wf.writelines("\n".join(','.join((key,val)) for (key,val) in INDEX.items()))

    JSON_values = []
    J_dict = {'URLs': {}}
    for key, val in INDEX.items():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        JSON_tuple = (key, val, now)
        JSON_values.append(JSON_tuple)
    for val in JSON_values:
        JSON_dict = Json_construct(*val)
        J_dict['URLs'].update(JSON_dict)
    update_json("WebHash.Json", J_dict)


def Json_construct(id,hash,date):
    website_dic = {id: {'properties': {}}}
    values = [{'hash': hash}, {'archival_date': date}]
    for val in values:
        website_dic[id]['properties'].update(val)
    return website_dic


def update_json(filename, data_dict):
    with open(filename, "w") as outfile:
        json_object = json.dumps(data_dict, indent=4)
        outfile.write(json_object)


def page_indexer(page_source, page_title):
    if not os.path.isfile(page_title + ".html"):
        print('New webpage code archive')
        with open(page_title + ".html", "w+") as file:
            file.write(page_source)
    elif os.path.isfile(page_title + ".html"):
        with open(page_title + "_new.html", "w+") as file:
            file.write(page_source)


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


def show_difference(old, new):
    f_old = open(old)
    old_text = f_old.readlines()
    f_new = open(new)
    new_text = f_new.readlines()
    print(Diff(old_text, new_text))


def page_checker(webpage_title):
        old = webpage_title + ".html"
        new = webpage_title + "_new.html"
        if os.path.isfile(old) and os.path.isfile(new):
            show_difference(old, new)
            os.remove(old)
            os.rename(new, webpage_title + ".html")
        else:
            print('relevant files does not exist')


def ad_blocker():
    all_iframes = DRIVER.find_elements(By.TAG_NAME, "iframe")
    if len(all_iframes) > 0:
        print("Ad Found\n")
        DRIVER.execute_script("""
            var elems = document.getElementsByTagName("iframe"); 
            for(var i = 0, max = elems.length; i < max; i++)
                 {
                     elems[i].hidden=true;
                 }
                              """)


def white_list_check():
    pass


def Website_change_checker():
    # Need to take into account first time storage
    whitelist = ['time']
    URL = "http://randomcolour.com/"
    srcOld = ""
    srcNew = ""
    while(1): # might need to store as a file to specific change
        try:
            srcOld = srcNew
            DRIVER.get(URL)
            WebDriverWait(DRIVER, 5)  # wait for webpage to load properly
            ad_blocker()
            srcNew = DRIVER.page_source  # get page source
            # might need to use html files or even try beautiful soup
            # print(srcNew)
            # print(srcOld)

            if srcNew != srcOld and srcOld == "":
                file = open("sample.html", "w+")
                file.write(srcNew)
                file.close()

            elif srcNew != srcOld and srcOld != "":
                print("website change")
                file = open("sample_new.html", "w+")
                file.write(srcNew)
                file.close()
                show_difference("sample.html", "sample_new.html")
                # os.remove("sample.html")
                # os.remove("sample_new.html")
                # Notify
                break

            elif srcNew == srcOld:
                print("No change")

        except:
            pass
        time.sleep(20)  # polling interval


def clean_urls(url_list):
    regex = re.compile(r'^.*\.(?!js$|ico$|atom$|png$)[^.]+$') # remove non-webpages
    filtered = [i for i in url_list if regex.match(i)]
    return filtered


def main():
    hash_indexer()
    url_crawled = crawler.Crawler('https://plainvanilla.com.sg/')
    get_web_source()
    archive_updater()
    # Website_change_checker()
    # print(list((url_crawled.crawled_urls)))
    print(clean_urls(list((url_crawled.crawled_urls))))


if __name__ == '__main__':
    main()
