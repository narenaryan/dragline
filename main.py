from gevent import monkey, spawn, joinall
monkey.patch_all()

import httplib2
import httpcache2
from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore
from urlparse import urljoin, urldefrag
from lxml import html
import sys
import os
import re


class Crawl(object):
    lock = BoundedSemaphore(1)
    current_urls = set()
    running_count = 0

    def __init__(self, module):
        self.url_queue = RedisQueue(module.NAME, 'urls')
        self.visited_urls = RedisSet(module.NAME, 'visited')
        self.url_pattern = re.compile(module.ALLOWED_URLS[0])
        for i in module.START_URLS:
            self.insert(i)
        self.http = httplib2.Http()
        self.parsers = module.PARSERS

    def count(self):
        return Crawl.running_count

    def inc_count(self, url):
        Crawl.lock.acquire()
        Crawl.current_urls.add(url)
        Crawl.running_count += 1
        Crawl.lock.release()

    def dec_count(self, url):
        Crawl.lock.acquire()
        Crawl.current_urls.remove(url)
        Crawl.running_count -= 1
        Crawl.lock.release()

    def insert(self, url):
        if not any(url in i for i in (Crawl.current_urls, self.visited_urls, self.url_queue)):
            self.url_queue.put(url)

    def parse(self, baseurl, content):
        data = html.fromstring(content)
        for url in data.xpath('//a/@href'):
            url = urldefrag(urljoin(baseurl, url))[0]
            if self.url_pattern.match(url):
                self.insert(url)

    def process_url(self):
        while True:
            url = self.url_queue.get(timeout=2)
            print url
            if url:
                self.inc_count(url)
                head, content = self.http.request(url, 'GET')
                self.parse(url, content)
                self.visited_urls.add(url)
                self.dec_count(url)
            else:
                if not self.count():
                    break


if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
    import main
    crawlers = []
    for i in xrange(5):
        crawler = Crawl(main)
        crawlers.append(spawn(crawler.process_url))
    joinall(crawlers)
    print "finished"
else:
    exit()
