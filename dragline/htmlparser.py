from lxml import etree
from urlparse import urldefrag, urljoin


class HtmlParser:

    def __init__(self, response):
        """
        :param response:
        :type response: :class:`Response`
        """
        self.url = response.url
        self.data = etree.HTML(response.body)

    def extract_urls(self, xpath=""):
        """
        This function extracts urls from a given xpath

        :param xpath: xpath from which the urls are to be fetched
        :type xpath: str
        :return: list of urls.

        >>> html = HtmlParser(response)
        >>> urls = html.extract_urls("EXAMPLE_XPATH")
        ['url1', 'url2', 'url3']

        """
        return [self.abs_url(self.url, url)
                for url in self.data.xpath(xpath + '//a/@href')]

    def xpath(self, xpath):
        """
        This function extracts contents of an xpath

        :param xpath: xpath of the content
        :type xpath: str
        """
        return self.data.xpath(xpath)

    def abs_url(self, baseurl, relativeurl):
        return urldefrag(urljoin(baseurl, relativeurl.strip()))[0]