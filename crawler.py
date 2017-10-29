import requests
import os
import re
import datetime
import time

import helpers
import filesystem
import crawler_queue
import crawler_cache

from urllib.parse import urlparse
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url, depth=1):
        self.__url = url

        if depth < 1:
            self.__depth = 1
        else:
            self.__depth = depth

        self.__domain = self.__extract_domain(url)
        self.__base_directory = helpers.slugify_filename(url) + '-' + str(depth)
        self.__download_directory = os.path.join(self.__base_directory, 'downloads')
        self.__results_file = 'results.tsv'
        self.__current_depth = 1

        filesystem.create_directory(self.__base_directory)
        filesystem.create_directory(self.__download_directory)

        self.__queue = crawler_queue.CrawlerQueue(helpers.slugify_filename(url), depth)
        self.__cache = crawler_cache.CrawlerCache()

    def __extract_domain(self, url):
        components = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=components)
        return domain

    def __download_page(self, url):
        filename = helpers.slugify_filename(url)
        path = os.path.join(self.__download_directory, filename)

        response = requests.get(url)
        response.encoding = 'utf-8'

        filesystem.write(path, response.text)

        return response.text

    def __should_download_page(self, url, response):
        if not self.__cache.is_visited(url):
            return True
        else:
            if 'Last-Modified' in response.headers:
                date_time = response.headers['Last-Modified']
                pattern = '%a, %d %b %Y %H:%M:%S %Z'
                epoch = int(time.mktime(time.strptime(date_time, pattern)))
                return epoch > self.__cache.get_last_modified(url)
            else:
                return True

    def __read_page_from_cache(self, url):
        filename = helpers.slugify_filename(url)
        path = os.path.join(self.__download_directory, filename)
        return filesystem.read(path)

    def __get_last_modified(self, url):
        data = self.__cache.get_last_modified(url)
        return data

    def __get_ratio(self, url):
        data = self.__cache.get_ratio(url)
        return data

    def __create_results_file(self):
        filesystem.create_file(os.path.join(self.__base_directory, self.__results_file))

    def __write_to_results_file(self, url, current_depth):
        path = os.path.join(self.__base_directory, self.__results_file)
        ratio = self.__cache.get_ratio(url)
        data = [url, current_depth, ratio]
        filesystem.append_to_csv(path, data)

    def crawl(self):

        if self.__queue.is_empty():
            self.__queue.put(self.__url, 1)
            self.__current_depth = 1
            self.__create_results_file()

        while not self.__queue.is_empty():

            current_url = self.__queue.get()
            self.__current_depth = current_url['depth']
            print("Working on:", current_url['url'], "Depth: ", self.__current_depth)

            response = requests.head(current_url['url'])
            if response.headers['content-type'] == 'text/html':

                should_download_page = self.__should_download_page(current_url['url'], response)
                if should_download_page:
                    page_contents = self.__download_page(current_url['url'])
                else:
                    page_contents = self.__read_page_from_cache(current_url['url'])

                parsed_html = BeautifulSoup(page_contents, 'html.parser')

                same_domain_count = 0
                links_count = 0

                for link in parsed_html.find_all('a', attrs={'href': re.compile("^http")}):
                    child_url = link.get('href')

                    if self.__current_depth < self.__depth:
                        self.__queue.put(child_url, self.__current_depth + 1)

                    if should_download_page:
                        if self.__extract_domain(child_url) == self.__domain:
                            same_domain_count += 1
                        links_count += 1

                if should_download_page:
                    print("Total URLs:", links_count)
                    print("Same domain:", same_domain_count)
                    print("Ratio: ", helpers.calculate_ratio(links_count, same_domain_count))

                    last_modified = int(datetime.datetime.utcnow().timestamp())

                    self.__cache.cache_url(current_url['url'],
                                           helpers.calculate_ratio(links_count, same_domain_count),
                                           last_modified)

                self.__write_to_results_file(current_url['url'], self.__current_depth)

            self.__queue.commit()
        print ("Results are located in ", os.path.abspath(self.__base_directory))
