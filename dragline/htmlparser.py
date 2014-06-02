from lxml import html
from urlparse import urldefrag, urljoin


class HtmlParser:

    def __init__(self, response):
        """
        :param response:
        :type response: :class:`dragline.http.Response`
        """
        self.data = html.fromstring(response.body, response.url)
        self.data.make_links_absolute()

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
        if xpath == "":
            return [url[2].split('#')[0] for url in self.data.iterlinks()]
        else:
            return [url.split('#')[0]
                    for url in self.data.xpath(xpath + '//a/@href')]

    def __getattr__(self, attr):
        return getattr(self.data, attr)
