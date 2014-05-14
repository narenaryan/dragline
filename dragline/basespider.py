import logging
class BaseSpider:
    def __init__(self):
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.REQUEST_HEADERS = {}
        self.initialize()

    def parse(self,baseurl,data):
        raise NotImplementedError

    def initialize(self):
        raise NotImplementedError




