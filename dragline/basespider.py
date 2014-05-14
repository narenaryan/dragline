import logging


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
