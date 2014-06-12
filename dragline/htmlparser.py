from lxml import html, etree
from parslepy import Parselet
from parslepy.funcs import xpathstrip
from urlparse import urldefrag, urljoin
from cssselect import HTMLTranslator
import re


ns = etree.FunctionNamespace(None)
ns['strip'] = xpathstrip


def links(self):
    urls = (url[2].split('#')[0] for url in self.iterlinks()
            if url[1] == 'href')
    return set(url for url in urls if re.match('^http://', url))


def extract_urls(self, xpath=''):
    if xpath:
        return set(url.split('#')[0] for url in self.xpath(xpath + "//a/@href")
                   if re.match('^http://', url))
    else:
        return self.links()


def gettext(self):
    return "".join(i.strip() for i in self.itertext())


def extract(self, rules):
    parselet = Parselet(rules)
    return parselet.extract(self, rules)


def cssselect(self, expr):
    return self._css_translator.css_to_xpath(expr)


def css(self, expr):
    return self.xpath(self.cssselect(expr))


html.HtmlElement.links = links
html.HtmlElement.gettext = gettext
html.HtmlElement._css_translator = HTMLTranslator()
html.HtmlElement.cssselect = cssselect
html.HtmlElement.css = css
html.HtmlElement.extract = extract
html.HtmlElement.extract_urls = extract_urls


def HtmlParser(response):
    """
    :param response:
    :type response: :class:`dragline.http.Response`

    This method takes response object as its argument and returns 
    the lxml etree object.
    
    HtmlParser function returns a lxml object of type Element which got 2 potential methods.
    All the details of lxml object are discussed in section `lxml Element object`_.
    """
    element = html.fromstring(response.body, response.url)
    element.make_links_absolute()
    return element
