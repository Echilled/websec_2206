import base64
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
import time

DRIVER = webdriver.Chrome("chromedriver.exe")
SITE = ["https://time.gov/", "https://www.ledr.com/colours/white.htm", "http://randomcolour.com/"]  # need test with same domain diff dir
INDEX = {}
times_url_change_dict = {}
DOM_CHANGES = {}
APP_PASSWORD = 'happymother123'


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
    page_changes_listing(DOM_CHANGES)
    # DRIVER.quit()


def web_hash_checker(url, md5):
    digest = md5.hexdigest()
    try:
        print(INDEX[url].strip('\n'), digest)
        if INDEX[url].strip('\n') != digest:
            INDEX[url] = digest
            print("Website does not match previous hash archive")  # Need user to accept before updating archive
            page_checker(DRIVER.title, url)
            # archive_updater()
        else:
            print("Website match previous archive")
            os.remove(DRIVER.title + "_new.html")
    except:
        INDEX[url] = digest
        print("New webpage archived")
        times_url_change_dict[url] = 0


def format_title(title):
    title = title.replace("|", "")
    return title


def index_change_history():
    with open("WebHash.Json", "r") as file:
        try:
            data = json.load(file)
            for url, property in data['URLs'].items():
                times_url_change_dict[url] = property['properties']['number of times URL content change']
                # print(properties)
        except Exception as e:
            print(e)
    return times_url_change_dict


def update_change_history():
    index_change_history()
    print(times_url_change_dict)
    for key in times_url_change_dict.keys():
        if key in DOM_CHANGES:
            times_url_change_dict[key] = times_url_change_dict.get(key, 0) + 1
    print(times_url_change_dict)


def archive_updater():
    # with open("WebHash.txt", "w+") as wf:
    print("Updating archive")
    # wf.writelines("\n".join(','.join((key,val)) for (key,val) in INDEX.items()))
    JSON_values = []   # Archive web page hash
    temp_dict = {'URLs': {}}
    update_change_history()
    for key, val in INDEX.items():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        changes_number = times_url_change_dict[key]
        JSON_tuple = (key, val, now, changes_number)
        JSON_values.append(JSON_tuple)
    for val in JSON_values:
        JSON_dict = json_construct(*val)
        temp_dict['URLs'].update(JSON_dict)
    update_json("WebHash.Json", temp_dict)
    for key in DOM_CHANGES.keys():  # Archive web page code
        DRIVER.get(key)
        page_title = format_title(DRIVER.title)
        old = page_title + ".html"
        new = page_title + "_new.html"
        os.remove(old)
        os.rename(new, page_title + ".html")


def json_construct(id, hash, date, times_it_changed):
    website_dic = {id: {'properties': {}}}
    values = [{'hash': hash}, {'archival_date': date}, {'number of times URL content change': times_it_changed}]
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
            return True
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
        new_changed_list.append(" ".join(difflib.get_close_matches(change, changed_list, 1)))
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
    try:
        if os.path.isfile(old) and os.path.isfile(new):
            DOM_CHANGES[url] = show_difference(old, new)
            # decision = input('Do u accept these changes? y/n')
            # if decision.lower() == 'y':
            #
            # elif decision.lower() == 'n':
            #     os.remove(new)
            # else:
            #     print('unrecognizable input, discarding changes')
            #     os.remove(new)
        else:
            print('relevant files does not exist, could be first time archiving')
    except Exception as e:
        print(e)


def page_changes_listing(changes_dict):
    if DOM_CHANGES:
        print('There are ' + str(len(changes_dict)) + ' url/s with changes')
        print('The URL/s with changes are:')
        for key in changes_dict.keys():
            print(key)
        print('Here are the changes:')
        for key, value in DOM_CHANGES.items():
            print('\n', key)
            print("Original content:")
            print(value[0])
            print("Changed content:")
            print(value[1])
        userinput = input("Do you accept these changes? y/n")  # only when user accepts, then the archive up beu updated
        if userinput.lower() == "y":
            archive_updater()
        if userinput.lower() == "n":
            print("changes discarded")
    else:
        print("there are no changes to any URLs")
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


def white_list_input(): # likely store in a file then retrieve the contents during check
    pass


def white_list_check(whitelist):
    pass


def periodic_check(time_interval_in_seconds):
    print("Polling every "+str(time_interval_in_seconds) + " seconds")
    while True:
        try:
                json_hash_indexer()
                get_web_source()
                time.sleep(time_interval_in_seconds)
        except Exception as e:
            print(e)


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
    # key = encrpyt_decrypt.derive_key(encrpyt_decrypt.generate_salt(), APP_PASSWORD)
    # base64.urlsafe_b64encode(key)
    # update_change_history()
    periodic_check(30)


if __name__ == '__main__':
    main()
