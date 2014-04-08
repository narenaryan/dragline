import re
import os
import sys
from lxml import etree
from urlparse import urljoin, urldefrag


class HtmlHandler:

    def __init__(self, allowed_urls, parser_module):
        self.url_pattern = re.compile(
            '(%s)' % '|'.join(self.compile_regex(i) for i in allowed_urls))
        self.parsers = self.load_parser(parser_module)

    def parse(self, head, baseurl, content):
        if "text/html" in head['content-type']:
            for parser in self.parsers:
                if parser.__regex__.match(baseurl):
                    parser.__process__(baseurl, content)
            data = etree.HTML(content)

            for url in data.xpath('//a/@href'):
                url = urldefrag(urljoin(baseurl, url.strip()))[0]
                if self.url_pattern.match(url):
                    yield url

    def load_parser(self, module):
        parsers = []
        dirname = os.path.dirname(module.__file__)
        sys.path.insert(0, dirname)
        for module in os.listdir(dirname):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            parser = __import__(module[:-3], locals(), globals())
            if not getattr(parser, '__regex__', None):
                continue
            parser.__regex__ = re.compile(self.compile_regex(parser.__regex__))
            parsers.append(parser)
        del sys.path[0]
        return parsers

    def compile_regex(self, regex):
        regex = re.escape(regex)
        regexpattern = [("NUM", "[0-9]+"), ("ALPHA", "[a-zA-Z]+"), (
            "ALPHANUM", "[0-9a-zA-Z]+"), ("ANY", ".+")]
        for pattern, replacement in regexpattern:
            regex = regex.replace(pattern, replacement)
        return regex
