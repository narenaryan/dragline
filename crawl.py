import time
import socket
import urllib
import httplib2
from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore
import json


class Crawl:

    def __init__(self, spider):
        self.lock = BoundedSemaphore(1)
        hash_func = lambda x: str(x['url'])
        self.current_urls = RedisSet(spider._name, 'current_urls', hash_func)
        self.running_count = 0
        self.url_queue = RedisQueue(spider._name, 'urls', json, hash_func)
        self.visited_urls = RedisSet(spider._name, 'visited', hash_func)
        self.spider = spider
        self.insert({"url": spider._start_url, "callback": "parse"})

    def count(self):
        return self.running_count

    def inc_count(self, url):
        self.lock.acquire()
        self.current_urls.add(url)
        self.running_count += 1
        self.lock.release()

    def dec_count(self, url):
        self.lock.acquire()
        self.running_count -= 1
        self.current_urls.remove(url)
        self.lock.release()

    def insert(self, url):
       
            if not any(url in i for i in (self.current_urls, self.visited_urls, self.url_queue)):
                self.url_queue.put(url)

         # self.url_queue.put(url)



class Crawler:

    def __init__(self):
        self.http = httplib2.Http(timeout=350)
        self.min_delay = 0.5
        self.max_delay = 300
        self.delay = self.min_delay + 5

    @classmethod
    def load_spider(Crawler, module):
        Crawler.crawl = Crawl(module)

    def process_url(self):
        retry = 0
        crawl = Crawler.crawl
        logger = crawl.spider.logger
        while True:
            if not retry:
                data = crawl.url_queue.get(timeout=2)
                print data
            else:
                logger.debug("Retrying %s for the %s time", data['url'], retry)
            if data:
                url = data['url']
                callback= data['callback']
                logger.debug("Processing url :%s", url)
                crawl.inc_count(data)
                try:

                    self.http.timeout = self.delay

                    time.sleep(self.delay)
                    start = time.time()
                    head, content = self.http.request(
                        urllib.quote(url, ":/?=&"), 'GET')
                    
                    callback =  getattr(crawl.spider,callback)

                    for urlinfo in callback(url,content):
                        crawl.insert(urlinfo)

                    end = time.time()
                except (httplib2.ServerNotFoundError, socket.timeout, socket.gaierror) as e:
                    self.http = httplib2.Http(timeout=self.delay)
                    retry = retry + 1 if retry < 3 else 0
                    if retry == 0:
                        logger.warning("Rejecting %s", url)
                        crawl.visited_urls.add(data)
                except Exception as e:
                    logger.error(
                        '%s: Failed to open the url %s', type(e), url, exc_info=True)
                    crawl.visited_urls.add(data)
                else:
                    retry = 0
                    logger.info("Finished processing %s", url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)
                    crawl.visited_urls.add(data)
                crawl.dec_count(data)

            else:
                if not crawl.count():
                    break
