from lxml import etree
from urlparse import urldefrag, urljoin


class HtmlParser:

    def __init__(self, url, content):
        self.url = url
        self.data = etree.HTML(content)

    def extract_urls(self, xpath):
        return [self.abs_url(self.url, url) for url in self.data.xpath(xpath + '//a/@href')]

    def extract(self, xpath):
        return self.data.xpath(xpath)

    def abs_url(self, baseurl, relativeurl):
        return urldefrag(urljoin(baseurl, relativeurl.strip()))[0]