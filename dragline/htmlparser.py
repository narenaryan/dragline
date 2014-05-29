from lxml import etree
from urlparse import urldefrag, urljoin


class HtmlParser:

    def __init__(self, response):
        self.url = response.url
        self.data = etree.HTML(response.body)

    def extract_urls(self, xpath):
        return [self.abs_url(self.url, url)
                for url in self.data.xpath(xpath + '//a/@href')]

    def xpath(self, xpath):
        return self.data.xpath(xpath)

    def abs_url(self, baseurl, relativeurl):
        return urldefrag(urljoin(baseurl, relativeurl.strip()))[0]
