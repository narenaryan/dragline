import logging
from urlparse import urljoin, urldefrag

class BaseSpider:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.REQUEST_HEADERS = {}
        self.initialize()

    def parse(self, baseurl, data):
        raise NotImplementedError

    def addLogHandler(self, handler):
        self.logger.addHandler(handler)

    def initialize(self):
        raise NotImplementedError

    def abs_url(baseurl, relativeurl):
        return urldefrag(urljoin(baseurl, url.strip()))[0]
