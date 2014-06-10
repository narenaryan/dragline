from lxml import html
from parslepy import Parselet
from urlparse import urldefrag, urljoin
from cssselect import HTMLTranslator
import re


def links(self):
    return set(url[2].split('#')[0] for url in self.iterlinks()
               if re.match('^http://', url) and url[1] == 'href')


def gettext(self):
    return "".join(i.strip for i in self.itertext())


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


def HtmlParser(response):
    """
    :param response:
    :type response: :class:`dragline.http.Response`
    """
    element = html.fromstring(response.body, response.url)
    element.make_links_absolute()
    return element
