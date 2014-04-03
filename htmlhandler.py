import re
from lxml import html

from urlparse import urljoin, urldefrag


class Parser:

    def __init__(self, allowed_urls, parsers):
        self.url_pattern = re.compile(
            '(%s)' % '|'.join(re.escape(i) for i in allowed_urls))
        self.parsers=parsers

    def parse(self, head, baseurl, content):
        #print baseurl
        if "text/html" in head['content-type']:
            data = html.fromstring(content)

            for parser in self.parsers:
                self.process(baseurl, parser, data)

            for url in data.xpath('//a/@href'):
                url = urldefrag(urljoin(baseurl, url.strip()))[0]
                if self.url_pattern.match(url):
                    yield url

    def process(self, baseurl,parser, data):
        
        if not re.match(re.escape(parser.__regex__),baseurl):
            return
        

        item = dict()
        for title, xpath in parser.__xpath__.items():
            item[title] = data.xpath(xpath)
        parser.__process__(item)
