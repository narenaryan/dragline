

import httplib2

from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore


import socket
import urllib
import time


class Crawl:

    def __init__(self, settings):
        self.lock = BoundedSemaphore(1)
        self.current_urls = RedisSet(settings.NAME,'current_urls')
        self.running_count = 0
        self.url_queue = RedisQueue(settings.NAME, 'urls')
        self.visited_urls = RedisSet(settings.NAME, 'visited')
        self.handler = HtmlHandler(settings)

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
                        urllib.quote(url, ":/?=&"), 'GET', headers=settings.REQUEST_HEADERS)

                    end = time.time()
                except (httplib2.ServerNotFoundError, socket.timeout,socket.gaierror) as e:
                    self.http = httplib2.Http(timeout=self.delay)
                    retry = retry + 1 if retry < 3 else 0
                    if retry == 0:
                        logger.warning("Rejecting %s", url)
                        crawl.visited_urls.add(url)
                except Exception, e:
                    logger.error(
                        '%s: Failed to open the url %s', type(e), url, exc_info=True)
                    crawl.visited_urls.add(url)
                else:
                    retry = 0
                    logger.info("Finished processing %s", url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)
                    if "content-location" in head:
                        url=head['content-location']
                        

                    for i in crawl.handler.parse(head, url, content):
                        crawl.insert(i)
                    crawl.visited_urls.add(url)
                crawl.dec_count(url)

            else:
                if not crawl.count():
                    break