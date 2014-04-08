from gevent import monkey, spawn, joinall
monkey.patch_all()

import httplib2
import httpcache2
from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore

import sys
import os
import re
import urllib
import time
from parsehandler import ParserHandler
import logging
from settings import Settings

settings = Settings()
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, settings['loglevel']))


class Crawl(object):
    lock = BoundedSemaphore(1)
    current_urls = set()
    running_count = 0

    def __init__(self):
        self.parser = Crawl.Parsers
        self.http = httplib2.Http(timeout=350)
        self.min_delay = 0.5
        self.max_delay = 300
        self.delay = self.min_delay + 5

    @classmethod
    def count(crawl):
        return crawl.running_count

    @classmethod
    def inc_count(crawl, url):
        crawl.lock.acquire()
        crawl.current_urls.add(url)
        crawl.running_count += 1
        crawl.lock.release()

    @classmethod
    def dec_count(crawl, url):
        crawl.lock.acquire()
        crawl.running_count -= 1
        crawl.lock.release()

    @classmethod
    def insert(crawl, url):
        if not any(url in i for i in (crawl.current_urls, crawl.visited_urls, crawl.url_queue)):
            crawl.url_queue.put(url)

    def process_url(self):
        retry = 0
        while True:

            if not retry:
                url = self.url_queue.get(timeout=2)
            else:
                logger.debug("Retrying %s for the %s time", url, retry)

            if url:
                logger.debug("Processing url :%s", url)
                self.inc_count(url)
                try:

                    self.http.timeout = self.delay

                    time.sleep(self.delay)
                    start = time.time()
                    head, content = self.http.request(
                        urllib.quote(url, ":/?=&"), 'GET', headers=settings['headers'])

                    end = time.time()
                except httplib2.ServerNotFoundError, e:
                    self.http = httplib2.Http(timeout=self.delay)
                    retry = retry + 1 if retry < 3 else 0
                    if retry == 0:
                        logger.debug("Rejecting %s", url)

                except Exception, e:
                    logger.error(
                        'Failed to open the url %s', url, exc_info=True)
                else:
                    retry = 0
                    logger.info("Finished processing %s", url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)

                    for i in self.parser.parse(head, url, content):
                        self.insert(i)
                    self.visited_urls.add(url)
                self.dec_count(url)

            else:
                if not self.count():
                    break


if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
else:
    logger.error("No spider specified")
    exit()

import main
Crawl.url_queue = RedisQueue(main.NAME, 'urls')
Crawl.visited_urls = RedisSet(main.NAME, 'visited')
Crawl.Parsers = ParserHandler(main.ALLOWED_URLS, main.PARSERS)
# if Crawl.url_queue.isempty():
#     Crawl.visited_urls.clear()
for url in main.START_URLS:
    Crawl.insert(url)
crawlers = []
for i in xrange(5):
    crawler = Crawl()
    crawlers.append(spawn(crawler.process_url))
try:
    joinall(crawlers)
except:
    logger.info("stopped %d threads", Crawl.running_count)
else:
    logger.info("finished")
