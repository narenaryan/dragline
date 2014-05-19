import logging
from urlparse import urljoin, urldefrag


class BaseSpider:
    def __init__(self, conf={}):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.REQUEST_HEADERS = {
            'content-type': "application/x-www-form-urlencoded"}
        self._conf = conf
        self.initialize()

    def parse(self, baseurl, data):
        raise NotImplementedError

    def addLogHandler(self, handler):
        self.logger.addHandler(handler)

    def initialize(self):
        raise NotImplementedError

    def abs_url(self, baseurl, relativeurl):
        return urldefrag(urljoin(baseurl, relativeurl.strip()))[0]
