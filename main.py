import httplib2
import httpcache2
from redisds import RedisQueue, RedisSet
from gevent import monkey, spawn
import sys
import os

monkey.patch_all()

class Crawl(object):
    lock = BoundedSemaphore(1)
    running_count = 0
    def __init__(self, module):
        self.url_queue = RedisQueue(module.name, 'urls')
        self.visited_urls = RedisSet(module.name, 'visited')
        for i in module.START_URLS:
            self.url_queue.put(i)
        http = httplib2.Http()

    def count(self):
        return running_count

    def inc_coubt(self):
        Crawl.lock.acquire()
        Crawl.running_count +=1
        Crawl.lock.release()

    def dec_coubt(self):
        Crawl.lock.acquire()
        Crawl.running_count -=1
        Crawl.lock.release()

    def process_url(self):
        self.url_queue.get(timeout=10)
        head, content = self.http.request(url, 'GET')


if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
    import main
    crawler = Crawl(main)
    spawn(crawler.process_url())
else:
    exit()