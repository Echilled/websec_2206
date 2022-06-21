import os
from difflib import Differ
from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
import hashlib
import time
import datetime
import json

DRIVER = webdriver.Chrome("chromedriver.exe")
SITE = ["http://www.beefychilled.tk/","http://randomcolour.com/", "https://www.ledr.com/colours/white.htm", "https://www.utctime.net/", "https://google.com"]
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
    with open("WebHash.txt", "w+") as wf:
        print("Updating archive")
        wf.writelines("\n".join(','.join((key,val)) for (key,val) in INDEX.items()))

    JSON_values = []
    J_dict = {'URLs': {}}
    for key,val in INDEX.items():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        JSON_tuple = (key,val, now)
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


def Website_code_checker():
    # Need to take into account first time storage
    URL = "https://www.utctime.net/"
    srcOld = ""
    srcNew = ""
    d = Differ()
    while(1):
        try:
            srcOld = srcNew
            DRIVER.get(URL)
            time.sleep(2)
            srcNew = DRIVER.page_source
            if srcNew != srcOld and srcOld != "":
                print("website change")

                # can use the differ class
            elif srcNew == srcOld:
                print("No change")
        except:
            pass
        time.sleep(20)


if __name__ == '__main__':
    # hash_indexer()
    # # print(INDEX)
    # get_web_source()
    # archive_updater()
    Website_code_checker()
