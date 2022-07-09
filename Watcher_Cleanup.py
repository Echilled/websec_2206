import difflib
import os
from selenium import webdriver
import hashlib
import time
import datetime
import json
import re
from selenium.webdriver.common.by import By
import encrpyt_decrypt

DRIVER = webdriver.Chrome("chromedriver.exe")
SITE = ["http://randomcolour.com/", "https://time.gov/"]  # need test with same domain diff dir
INDEX = {}
DOM_CHANGES = {}
APP_PASSWORD = 'happy'


def json_hash_indexer():
    with open("WebHash.Json", "r") as file:
        try:
            data = json.load(file)
            for url, property in data['URLs'].items():
                INDEX[url] = property['properties']['hash']
                # print(properties)
        except:
            pass


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
            page_checker(DRIVER.title, url)
        else:
            print("Website match previous archive")
            os.remove(DRIVER.title + "_new.html")
    except:
        INDEX[url] = digest
        print("New webpage archived")


def format_title(title):
    title = title.replace("|", "")
    return title


def archive_updater():
    # with open("WebHash.txt", "w+") as wf:
    print("Updating archive")
    # wf.writelines("\n".join(','.join((key,val)) for (key,val) in INDEX.items()))

    JSON_values = []
    temp_dict = {'URLs': {}}
    for key, val in INDEX.items():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        JSON_tuple = (key, val, now)
        JSON_values.append(JSON_tuple)
    for val in JSON_values:
        JSON_dict = jon_construct(*val)
        temp_dict['URLs'].update(JSON_dict)
    update_json("WebHash.Json", temp_dict)


def jon_construct(id, hash, date):
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
    page_title = format_title(page_title)
    if not os.path.isfile(page_title + ".html"):
        print('New webpage code archive')
        with open(page_title + ".html", "w+") as file:
            file.write(page_source)
    elif os.path.isfile(page_title + ".html"):
        with open(page_title + "_new.html", "w+") as file:
            file.write(page_source)


def Diff(li1, li2):
    new_changed_list = []
    changes_list = []
    previous_list = list(set(li1) - set(li2))
    changed_list = list(set(li2) - set(li1))
    # changes_list = list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    # print(previous_list)
    # print(changed_list)
    for change in previous_list:
        new_changed_list.append(
            " ".join(difflib.get_close_matches(change, changed_list, 1)))
    print(previous_list)
    print(new_changed_list)
    changes_list.append(previous_list)
    changes_list.append(new_changed_list)
    return changes_list


def show_difference(old, new):
    f_old = open(old)
    old_text = f_old.readlines()
    f_new = open(new)
    new_text = f_new.readlines()
    return Diff(old_text, new_text)


def page_checker(webpage_title, url):
    webpage_title = format_title(webpage_title)
    old = webpage_title + ".html"
    new = webpage_title + "_new.html"
    if os.path.isfile(old) and os.path.isfile(new):
        DOM_CHANGES[url] = show_difference(old, new)
        decision = input('Do u accept these changes? y/n')
        if decision.lower() == 'y':
            os.remove(old)
            os.rename(new, webpage_title + ".html")
        elif decision.lower() == 'n':
            os.remove(new)
        else:
            print('unrecognizable input, discarding changes')
            os.remove(new)
    else:
        print('relevant files does not exist')


def page_changes_listing(changes_dict):
    print('There are ' + str(len(changes_dict)) + ' urls with changes')
    print('The URLs with changes are:')
    for key in changes_dict.keys():
        print(key)
    # print('If you want to accept all changes, press 0')
    # decision = input('Enter you choice')
    # print(decision)


def ad_blocker():
    all_iframes = DRIVER.find_elements(By.TAG_NAME, "iframe")
    if len(all_iframes) > 0:
        print("Ad Found, changes detected may contain ads\n")
        DRIVER.execute_script("""
            var elems = document.getElementsByTagName("iframe"); 
            for(var i = 0, max = elems.length; i < max; i++)
                 {
                     elems[i].hidden=true;
                 }
                              """)


def report_generation():
    pass


def white_list_check():
    pass


def periodic_check(time_interval):
    pass


def clean_urls(url_list):
    regex = re.compile(
        r'^.*\.(?!js$|ico$|atom$|png$)[^.]+$')  # remove non-webpages
    filtered = [i for i in url_list if regex.match(i)]
    return filtered


def main():
    # json_hash_indexer()
    # # url_crawled = crawler.Crawler('https://plainvanilla.com.sg/')
    # get_web_source()
    # archive_updater()
    # page_changes_listing(DOM_CHANGES)
    # print(DOM_CHANGES)
    # print(clean_urls(list((url_crawled.crawled_urls))))
    print(encrpyt_decrypt.derive_key(encrpyt_decrypt.generate_salt(), "Random colour.html"))


if __name__ == '__main__':
    main()
