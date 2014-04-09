from gevent import monkey, spawn, joinall
monkey.patch_all()

import httplib2
import httpcache2
from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore

import sys
import os
import socket
import re
import urllib
import time
from htmlhandler import HtmlHandler
import logging
from settings import Settings

settings = Settings()
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, settings['loglevel']))


class Crawl:

    def __init__(self, main):
        self.lock = BoundedSemaphore(1)
        self.current_urls = set()
        self.running_count = 0
        self.url_queue = RedisQueue(main.NAME, 'urls')
        self.visited_urls = RedisSet(main.NAME, 'visited',hash_func=None)
        self.handler = HtmlHandler(main.ALLOWED_URLS, main.PARSER_MODULE)

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
        self.lock.release()

    def insert(self, url):

        if not any(url in i for i in (self.current_urls,self.visited_urls, self.url_queue)):
            self.url_queue.put(url)


class Crawler:

    def __init__(self):
        self.http = httplib2.Http(timeout=350)
        self.min_delay = 0.5
        self.max_delay = 300
        self.delay = self.min_delay + 5

    def process_url(self, crawl):
        retry = 0
        while True:

            if not retry:
                url = crawl.url_queue.get(timeout=2)
            else:
                logger.debug("Retrying %s for the %s time", url, retry)
            if url:
                logger.debug("Processing url :%s", url)
                crawl.inc_count(url)
                try:

                    self.http.timeout = self.delay

                    time.sleep(self.delay)
                    start = time.time()
                    head, content = self.http.request(
                        urllib.quote(url, ":/?=&"), 'GET', headers=settings['headers'])

                    end = time.time()
                except httplib2.ServerNotFoundError,socket.timeout:
                    self.http = httplib2.Http(timeout=self.delay)
                    retry = retry + 1 if retry < 3 else 0
                    if retry == 0:
                        logger.debug("Rejecting %s", url)
                


                except Exception, e:
                    print "type is ",type(e)
                    logger.error(
                        'Failed to open the url %s', url, exc_info=True)
                

                else:
                    retry = 0
                    logger.info("Finished processing %s", url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)
                    for i in crawl.handler.parse(head,head['content-location'], content):
                        crawl.insert(i)
                    crawl.visited_urls.add(url)
                crawl.dec_count(url)

            else:
                if not crawl.count():
                    break


if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
    import main
    del sys.path[0]
else:
    logger.error("No spider specified")
    exit()

crawl = Crawl(main)
for url in main.START_URLS:
    crawl.insert(url)
try:
    crawlers = [Crawler() for i in xrange(5)]
    joinall([spawn(crawler.process_url, crawl) for crawler in crawlers])
except:
    logger.info("stopped %d threads", crawl.count(), exc_info=True)
else:
    logger.info("finished")
