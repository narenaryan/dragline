import re
import os
import sys
from lxml import etree
from urlparse import urljoin, urldefrag
import logging




class HtmlHandler:

    def __init__(self, settings):
        self.logger=settings.log
        self.url_pattern = re.compile(
            '(%s)' % '|'.join(self.compile_regex(i) for i in settings.ALLOWED_URLS))
        self.parsers = self.load_parser(settings.PARSER_MODULE)
        self.settings = settings
        

    def parse(self, head, baseurl, content):
        if "text/html" in head['content-type']:
            for parser in self.parsers:
                if parser.__regex__.match(baseurl):
                    try:
                        parser.__process__(baseurl, content)
                    except:
                        self.logger.error(
                            "Failed to parse %s", baseurl, exc_info=True)
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
            try:
                parser = __import__(module[:-3], locals(), globals())
            except:
                self.logger.error("Failed to load paser  %s", module, exc_info=True)
                continue

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
