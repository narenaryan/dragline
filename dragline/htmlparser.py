from lxml import html
from urlparse import urldefrag, urljoin


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
        return [url[2].split('#')[0] for url in self.iterlinks()]
    else:
        return [url.split('#')[0]
                for url in self.xpath(xpath + '//a/@href')]

html.HtmlElement.extract_urls = extract_urls


def HtmlParser(response):
    """
    :param response:
    :type response: :class:`dragline.http.Response`
    """
    element = html.fromstring(response.body, response.url)
    element.make_links_absolute()
    return element
