import re
from lxml import html

from urlparse import urljoin, urldefrag

class Parser:

    def __init__(self, allowed_urls):
        self.url_pattern = re.compile(
            '(%s)' % '|'.join(re.escape(i) for i in allowed_urls))

    def parse(self, head,baseurl, content):
        if "text/html" in head['content-type']:
            data = html.fromstring(content)
            for url in data.xpath('//a/@href'):
                url = urldefrag(urljoin(baseurl, url.strip()))[0]
                if self.url_pattern.match(url):
                    yield url
