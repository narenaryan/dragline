from gevent import monkey, spawn, joinall
monkey.patch_all()

import httplib2
import httpcache2
from redisds import RedisQueue, RedisSet
from gevent.coros import BoundedSemaphore

from lxml import html
import sys
import os
import re
import urllib
import time
import traceback
from parsehandler import ParserHandler
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
# handler = logging.FileHandler('hello.log')
# handler.setLevel(logging.DEBUG)

# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # add the handlers to the logger
# logger.addHandler(handler)



agents = ['Mozilla/1.22 (compatible; MSIE 2.0d; Windows NT)',
          'Mozilla/2.0 (compatible; MSIE 3.02; Update a; Windows NT)',
          'Mozilla/4.0 (compatible; MSIE 4.01; Windows NT)',
          'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0)',
          'Mozilla/4.79 [en] (WinNT; U)',
          'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:0.9.2) Gecko/20010726 Netscape6/6.1',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
          'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14',
          'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaE90-1/210.34.75 Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
          'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_2 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5G77 Safari/525.20',
          'Mozilla/5.0 (Linux; U; Android 1.5; en-gb; HTC Magic Build/CRB17) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1',
          'Opera/9.27 (Windows NT 5.1; U; en)',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
          'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.4.154.25 Safari/525.19',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
          'Wget/1.8.2',
          'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
          'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; (R1 1.6))',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1',
          'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10 (.NET CLR 3.5.30729) JBroFuzz/1.4',
          'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
          'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20050923 CentOS/1.0.7-1.4.1.centos4 Firefox/1.0.7',
          'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727)',
          'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5',
          'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.7) Gecko/20070606',
          'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.14) Gecko/20080520 Firefox/2.0.0.14',
          'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.5) Gecko/2008120121 Firefox/3.0.5']


class Crawl(object):
    lock = BoundedSemaphore(1)
    current_urls = set()
    running_count = 0

    def __init__(self):

        self.parser = Crawl.Parsers
        self.http = httplib2.Http(timeout=350)
        print dir(self.http)
        print self.http.timeout
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
            # print "found", #
            crawl.url_queue.put(url)

    def process_url(self):
        retry = 0
        while True:

            if not retry:
                url = self.url_queue.get(timeout=2)
            else:
                #print "retrying ", url, "for ", retry, " time"
                logger.debug("Retrying %s for the %s time",url,retry)

            if url:
                #print "processing", url
                logger.debug("Processing url :%s",url)
                self.inc_count(url)
                try:

                    self.http.timeout = self.delay
                    print "current delay is ", self.delay

                    time.sleep(self.delay)
                    start = time.time()

                    headers = {"user-agent": agents[5], "accept-encoding": "gzip,deflate,sdch", "accept-language":
                               "en-US,en;q=0.8", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
                    head, content = self.http.request(
                        urllib.quote(url, ":/?=&"), 'GET')

                    end = time.time()
                except httplib2.ServerNotFoundError, e:
                    self.http = httplib2.Http(timeout=self.delay)
                    retry = retry + 1 if retry < 3 else 0
                    if retry==0:
                        logger.debug("Rejecting %s",url)

                    # print "processed", url
                except Exception, e:
                    print "failed", url, traceback.format_exc()
                else:
                    retry = 0
                    logger.info("Finished processing %s",url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)
                   # new_delay = min(max(self.mindelay, latency, (slot.delay + latency) / 2.0), self.maxdelay)

                    for i in self.parser.parse(head, url, content):
                        self.insert(i)
                    self.visited_urls.add(url)
                self.dec_count(url)

            else:
                print self.count()
                if not self.count():
                    break


if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
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
    joinall(crawlers)
    print "finished"
else:
    exit()
