import time



import redisds
import json
import re
import logging






class Crawl:

    def __init__(self, spider, settings):
        self.url_set = redisds.Set('urlset', spider._name,)
        self.url_queue = redisds.Queue('urlqueue', spider._name, json)
        self.running_count = redisds.Counter("count", namespace=spider._name)
        self.allowed_urls_regex = re.compile(spider._allowed_urls_regex)
        self.spider = spider
        self.settings = settings

    def start(self, resume):
        if not resume and self.count() == 0:
            self.url_queue.clear()
            self.url_set.clear()
        if 'callback' not in self.spider._start:
            self.spider._start['callback'] = "parse"
        self.insert(self.spider._start)

    def count(self):
        return self.running_count.get()

    def inc_count(self):
        self.running_count.inc()

    def decr_count(self):
        self.running_count.decr()

    def insert(self, data):
        data['method'] = data.get("method", "GET")
        data['form-data'] = data.get("form-data", {})
        if data['method'] == "GET":
            urlhash = usha1(data['url'])
        else:
            params = json.dumps([data['method'], data["url"], data["form-data"]])
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
    def load_spider(Crawler, module, resume, settings):
        Crawler.crawl = Crawl(module, settings)
        Crawler.crawl.start(resume)

    def process_url(self):
        retry = 0
        crawl = Crawler.crawl
        logger = logging.getLogger("dragline")
        while True:
            if not retry:
                data = crawl.url_queue.get(timeout=2)
            else:
                logger.debug("Retrying %s for the %s time", data['url'], retry)
            if data:
                url = data['url']

                logger.info("Processing url :%s", url)
                if not retry:
                    crawl.inc_count()
                try:
                    self.http.timeout = self.delay
                    time.sleep(self.delay)
                    start = time.time()
                    data["head"], content = self.http.request(
                        url, data['method'],
                        headers=data.get(
                            'headers', crawl.settings.REQUEST_HEADERS),
                        body=urllib.urlencode(data["form-data"]))
                    try:
                        parser_function = getattr(
                            crawl.spider, data['callback'])
                        try:
                            meta = data['meta']
                        except:
                            meta = None
                        urls = parser_function(data, content,meta)
                    except:
                        logger.exception("Failed to execute callback function")
                        urls = None
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
                    logger.exception(
                        '%s: Failed to open the url %s', type(e), url)
                else:
                    retry = 0
                    logger.info("Finished processing %s", url)
                    self.delay = min(
                        max(self.min_delay, end - start, (self.delay + end - start) / 2.0), self.max_delay)
                if not retry:
                    crawl.decr_count()
            else:
                if crawl.count() == 0:
                    break
                logger.debug("Waiting for %s", crawl.count())
