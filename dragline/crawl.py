from dragline import __version__
try:
    from cPickle import Pickler, Unpickler, HIGHEST_PROTOCOL
except:
    from pickle import Pickler, Unpickler, HIGHEST_PROTOCOL
import re
from defaultsettings import CrawlSettings, RequestSettings
from defaultsettings import SpiderSettings, LogSettings
from . import redisds
from gevent.coros import BoundedSemaphore
from .http import Request, RequestError
from uuid import uuid4
from datetime import datetime
from pytz import timezone

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class Pickle():

    def dumps(self, obj, protocol=HIGHEST_PROTOCOL):
        file = StringIO()
        Pickler(file, protocol).dump(obj)
        return file.getvalue()

    def loads(self, str):
        file = StringIO(str)
        return Unpickler(file).load()


class Crawler:
    settings = CrawlSettings()

    def __init__(self, spider_class, settings):
        def get(value, default={}):
            try:
                return getattr(settings, value)
            except AttributeError:
                return default
        self.settings = CrawlSettings(get('CRAWL'))
        Request.settings = RequestSettings(get('REQUEST'))
        spider_settings = SpiderSettings(get('SPIDER'))
        spider = spider_class(spider_settings)
        log = LogSettings(get('LOGFORMATTERS'), get('LOGHANDLERS'),
                          get('LOGGERS'))
        spider.logger = log.getLogger(spider.name)
        self.logger = log.getLogger(spider.name)
        self.load(spider)
        Request.stats = self.stats

    def load(self, spider):
        redis_args = dict(host=self.settings.REDIS_URL,
                          port=self.settings.REDIS_PORT,
                          db=self.settings.REDIS_DB)
        if hasattr(self.settings, 'NAMESPACE'):
            redis_args['namespace'] = self.settings.NAMESPACE
        else:
            redis_args['namespace'] = spider.name
        self.url_set = redisds.Set('urlset', **redis_args)
        self.url_queue = redisds.Queue('urlqueue', serializer=Pickle(),
                                       **redis_args)
        self.runner = redisds.Lock("runner:%s" % uuid4().hex, **redis_args)
        self.runners = redisds.Dict("runner:*", **redis_args)
        self.stats = redisds.Dict("stats:*", **redis_args)
        self.lock = BoundedSemaphore(1)
        self.running_count = 0
        self.allowed_urls_regex = self.get_regex(spider.allowed_domains)
        self.spider = spider
        self.start()

    def get_regex(self, domains):
        default = (r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                   r'localhost|'  # localhost...
                   r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                   r'(?::\d+)?')
        domain_regex = r'(%s)' % '|'.join(domains) if len(domains) else default
        url_regex = r'^https?://%s(?:/?|[/?]\S+)$' % domain_regex
        regex = re.compile(url_regex, re.IGNORECASE)
        return regex

    def current_time(self):
        tz = timezone(self.settings.TIME_ZONE)
        return datetime.now(tz).isoformat()

    def start(self):
        if not self.settings.RESUME and self.completed():
            self.url_queue.clear()
            self.url_set.clear()
        if self.url_queue.empty():
            self.stats.clear()
        if isinstance(self.spider.start, list):
            requests = self.spider.start
        else:
            requests = [self.spider.start]
        for request in requests:
            if isinstance(request, str):
                request = Request(request)
            if request.callback is None:
                request.callback = "parse"
            self.insert(request)
        self.stats['status'] = "running"
        self.stats['start_time'] = self.current_time()

    def clear(self, finished):
        self.runner.release()
        if finished:
            self.stats['status'] = 'finished'
            self.url_queue.clear()
            self.url_set.clear()
        elif self.completed():
            self.stats['end_time'] = self.current_time()
            self.stats['status'] = 'stopped'
        stats = dict(self.stats)
        stats['runners'] = len(self.runners)
        self.logger.info("%s", str(stats))

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
        self.url_queue.put(request)
        del request

    def process_url(self):
        while True:
            request = self.url_queue.get(timeout=2)
            if request:
                self.logger.info("Processing %s", request)
                self.inc_count()
                try:
                    response = request.send()
                    try:
                        callback = getattr(self.spider, request.callback)
                        requests = callback(response)
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        self.logger.exception("Failed to execute callback")
                        requests = None
                    if requests:
                        for i in requests:
                            self.insert(i)
                except RequestError as e:
                    request.retry += 1
                    if request.retry >= self.settings.MAX_RETRY:
                        self.logger.warning("Rejecting %s", request)
                    else:
                        self.logger.debug("Retrying %s", request)
                        self.insert(request, False)
                # except Exception as e:
                # self.logger.exception('Failed to open the url %s', request)
                except KeyboardInterrupt:
                    self.insert(request, False)
                    raise KeyboardInterrupt
                else:
                    self.logger.info("Finished processing %s", request)
                finally:
                    self.decr_count()
            else:
                if self.completed():
                    break
                self.logger.info("Waiting for %s", self.running_count)
