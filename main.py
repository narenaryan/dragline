import httplib2
import httpcache2
from redisds import RedisQueue, RedisSet
import sys
import os

if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
    import main
    print main.START_URLS
else:
    exit()

http = httplib2.Http()
url_queue = RedisQueue(main.NAME, 'urls')
visited_urls = RedisSet(main.NAME, 'visited')


def process_url(url):
    head, content = http.request(url, 'GET')
    print head