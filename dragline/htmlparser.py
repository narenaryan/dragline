from lxml import html, etree
from parslepy import Parselet
from parslepy.funcs import xpathstrip
from urlparse import urldefrag, urljoin
from cssselect import HTMLTranslator
import re


ns = etree.FunctionNamespace(None)
ns['strip'] = xpathstrip


def extract_urls(self, xpath=''):
    if xpath and not xpath.endswith('/'):
        xpath.append('/')
    return set(url.split('#')[0] for url in
               self.xpath(xpath + "descendant-or-self::a/@href")
               if re.match('^http://', url))


def extract_text(self):
    return "".join(i.strip() for i in self.itertext())


def extract(self, rules):
    parselet = Parselet(rules)
    return parselet.extract(self, rules)


def cssselect(self, expr):
    return self._css_translator.css_to_xpath(expr)


def css(self, expr):
    return self.xpath(self.cssselect(expr))


html.HtmlElement.extract_text = extract_text
html.HtmlElement._css_translator = HTMLTranslator()
html.HtmlElement.cssselect = cssselect
html.HtmlElement.css = css
html.HtmlElement.extract = extract
html.HtmlElement.extract_urls = extract_urls


def HtmlParser(response):
    """
    :param response:
    :type response: :class:`dragline.http.Response`
    """
    element = html.fromstring(response.body, response.url)
    element.make_links_absolute()
    return element
