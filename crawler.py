import logging
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, SoupStrainer
from ordered_set import OrderedSet
from helpers import is_url_valid, get_clean_url, is_link_internal

logging.basicConfig(
    filename='log.txt',
    filemode='a',
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
    )

class Crawler:

    def __init__(self, url, depth=25):
        self.crawled_urls = OrderedSet([])
        if (is_url_valid(url)):
            url = get_clean_url(url, '')
            self.depth = depth
            self.index = 0
            self.crawled_urls.add(url)
            self.crawl(url)

    def crawl(self, url):
        '''
        Crawl over URLs
            - scrape for anchor tags with hrefs in a webpage
            - reject if unwanted or cleanup the obtained links
            - append to a set to remove duplicates
            - "crawled_urls" is the repository for crawled URLs
        @input:
            url: URL to be scraped
        '''
        found_urls = []
        try:
            page = urlopen(Request(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
                    }
                ))

            content = page.read()
            '''
            # To save webpage as file (Use when defacement check is implemented)
            with open(f'backend/saved_pages/{url.split("//")[1]}.html', 'w') as f:
                f.write(content.decode('utf-8'))
            '''
            soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer(['a', 'link']))
            for anchor in soup.find_all(['a', 'link']):
                link = anchor.get('href')
                if is_url_valid(link):
                    # Complete relative URLs
                    link = get_clean_url(url, link)
                    if is_link_internal(link, url):
                        found_urls.append(link)

            soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer(['script', 'img']))
            for anchor in soup.find_all(['script', 'img']):
                link = anchor.get('src')
                if is_url_valid(link):
                    # Complete relative URLs
                    link = get_clean_url(url, link)
                    if is_link_internal(link, url):
                        found_urls.append(link)

        except HTTPError as e:
            print('HTTPError:' + str(e.code) + ' in ', url)
        except URLError as e:
            print('URLError: ' + str(e.reason) + ' in ', url)
        except Exception:
            import traceback
            print('Generic exception: ' + traceback.format_exc() + ' in ', url)

        cleaned_found_urls = set(found_urls)  # To remove repitions
        self.crawled_urls |= cleaned_found_urls  # Union of sets
        #if (len(self.crawled_urls) > self.depth):
            #self.crawled_urls = self.crawled_urls[:self.depth]
            #return
        #else:
        # Crawl the crawled urls
        self.index += 1
        if self.index < len(self.crawled_urls):
            url = self.crawled_urls[self.index]
            self.crawl(url)
            logging.info(f'Crawling: {url}')
        else:
            return
    


#if __name__ == '__main__':
#    Crawler('https://plainvanilla.com.sg/')
