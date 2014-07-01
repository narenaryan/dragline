import json
import re
from defaultsettings import CrawlSettings, RequestSettings
from defaultsettings import SpiderSettings, LogSettings
from . import redisds
from gevent.coros import BoundedSemaphore
from .http import Request, RequestError
from uuid import uuid4
from datetime import datetime
from pytz import timezone


class Crawl:
    settings = CrawlSettings()

    def __init__(self, spider):
        redis_args = dict(host=self.settings.REDIS_URL,
                          port=self.settings.REDIS_PORT,
                          db=self.settings.REDIS_DB)
        if hasattr(self.settings, 'NAMESPACE'):
            redis_args['namespace'] = self.settings.NAMESPACE
        else:
            redis_args['namespace'] = spider._name
        self.url_set = redisds.Set('urlset', **redis_args)
        self.url_queue = redisds.Queue('urlqueue', serializer=json,
                                       **redis_args)
        self.runner = redisds.Lock("runner:%s" % uuid4().hex, **redis_args)
        self.runners = redisds.Dict("runner:*", **redis_args)
        self.stats = redisds.Dict("stats:*", **redis_args)
        self.lock = BoundedSemaphore(1)
        self.running_count = 0
        self.allowed_urls_regex = re.compile(spider._allowed_urls_regex)
        self.spider = spider
        self.start()

    def __current_time(self):
        tz = timezone(self.settings.TIME_ZONE)
        return datetime.now(tz).isoformat()

    def start(self):
        if not self.settings.RESUME and self.completed():
            self.url_queue.clear()
            self.url_set.clear()
        if self.url_queue.empty():
            self.stats.clear()
        request = self.spider._start
        if request.callback is None:
            request.callback = "parse"
        self.insert(request)
        self.stats['status'] = "running"
        self.stats['start_time'] = self.__current_time()

    def clear(self, finished):
        self.runner.release()
        self.stats['end_time'] = self.__current_time()
        self.stats['status'] = 'stopped'
        if finished:
            self.stats['status'] = 'finished'
            self.url_queue.clear()
            self.url_set.clear()
        self.logger.info("%s", str(dict(self.stats)))

    def completed(self):
        return len(self.runners) == 0

    def inc_count(self):
        self.lock.acquire()
        if self.running_count == 0:
            self.runner.acquire()
        self.running_count += 1
        self.lock.release()

    def decr_count(self):
        self.lock.acquire()
        self.running_count -= 1
        if self.running_count == 0:
            self.runner.release()
        self.lock.release()

    def insert(self, request, check=True):
        if not isinstance(request, Request):
            return
        reqhash = request.get_unique_id()
        if check:
            if not self.allowed_urls_regex.match(request.url):
                return
            elif reqhash in self.url_set:
                return
        self.url_set.add(reqhash)
        self.url_queue.put(request.__dict__)
        del request


class Crawler():

    @classmethod
    def load_spider(Crawler, spider_class, settings):
        def get(value, default={}):
            try:
                return getattr(settings, value)
            except AttributeError:
                return default
        Crawl.settings = CrawlSettings(get('CRAWL'))
        Request.settings = RequestSettings(get('REQUEST'))
        spider_settings = SpiderSettings(get('SPIDER'))
        spider = spider_class(spider_settings)
        log = LogSettings(get('LOGFORMATTERS'), get('LOGHANDLERS'),
                          get('LOGGERS'))
        Crawl.logger = log.getLogger("dragline")
        spider.logger = log.getLogger(spider._name)
        Crawler.logger = log.getLogger(spider._name)
        Crawler.crawl = Crawl(spider)

    def process_url(self):
        crawl = Crawler.crawl
        request = Request(None)
        while True:
            args = crawl.url_queue.get(timeout=2)
            if args:
                request._set_state(args)
                self.logger.info("Processing %s", request)
                crawl.inc_count()
                try:
                    response = request.send()
                    crawl.stats['pages_crawled'] += 1
                    crawl.stats['request_bytes'] += len(response)
                    try:
                        callback = getattr(crawl.spider, request.callback)
                        requests = callback(response)
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        self.logger.exception("Failed to execute callback")
                        requests = None
                    if requests:
                        for i in requests:
                            crawl.insert(i)
                except RequestError as e:
                    request.retry += 1
                    if request.retry >= crawl.settings.MAX_RETRY:
                        self.logger.warning("Rejecting %s", request)
                    else:
                        self.logger.debug("Retrying %s", request)
                        crawl.insert(request, False)
                # except Exception as e:
                #    self.logger.exception('Failed to open the url %s', request)
                except KeyboardInterrupt:
                    crawl.insert(request, False)
                    raise KeyboardInterrupt
                else:
                    self.logger.info("Finished processing %s", request)
                finally:
                    crawl.decr_count()
            else:
                if crawl.completed():
                    break
                self.logger.debug("Waiting for %s", crawl.running_count)
