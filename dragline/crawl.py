import time
import socket
import urllib
import httplib2
from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore
import json
import re
from hashlib import sha1


def usha1(x):
    """sha1 with unicode support"""
    if isinstance(x, unicode):
        return sha1(x.encode('utf-8')).hexdigest()
    else:
        return sha1(x).hexdigest()


class Crawl:

    def __init__(self, spider):
        self.lock = BoundedSemaphore(1)
        self.url_set = RedisSet(spider._name, 'current_urls')
        self.url_queue = RedisQueue(spider._name, 'urls', json)
        self.allowed_urls_regex = re.compile(spider._allowed_urls_regex)
        self.running_count = 0
        self.spider = spider
        self.insert({"url": spider._start_url, "callback": "parse"})

    def count(self):
        return self.running_count

    def dec_count(self):
        self.lock.acquire()
        self.running_count += 1
        self.lock.release()

    def inc_count(self):
        self.lock.acquire()
        self.running_count -= 1
        self.lock.release()

    def insert(self, data):
        method = data.get("method", "GET")
        if method == "GET":
            urlhash = usha1(data['url'])
        else:
            params = json.dumps(["method", data["url"], data["form-data"]])
            urlhash = usha1(params)
        if self.allowed_urls_regex.match(data['url']) and urlhash not in self.url_set:
            self.url_set.add(urlhash)
            self.url_queue.put(data)


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
            else:
                logger.debug("Retrying %s for the %s time", data['url'], retry)
            if data:
                url = data['url']
                logger.debug("Processing url :%s", url)
                crawl.inc_count()
                try:
                    self.http.timeout = self.delay
                    time.sleep(self.delay)
                    start = time.time()
                    head, content = self.http.request(
                        urllib.quote(url, ":/?=&"), 'GET')
                    parser_function = getattr(crawl.spider, data['callback'])
                    urls = parser_function(url, content)
                    if urls:
                        for i in urls:
                            crawl.insert(i)
                    end = time.time()
                except (httplib2.ServerNotFoundError, socket.timeout, socket.gaierror) as e:
                    self.http = httplib2.Http(timeout=self.delay)
                    retry = retry + 1 if retry < 3 else 0
                    if retry == 0:
                        logger.warning("Rejecting %s", url)
                except Exception as e:
                    logger.exception('%s: Failed to open the url %s', type(e), url)
                else:
                    retry = 0
                    logger.info("Finished processing %s", url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)
                crawl.dec_count()
            else:
                if not crawl.count():
                    break
