import re
from lxml import etree
from urlparse import urljoin, urldefrag


class ParserHandler:

    def __init__(self, allowed_urls, parsers):
        print len(parsers)
        self.url_pattern = re.compile(
            '(%s)' % '|'.join(self.compile_regex(i) for i in allowed_urls))
        for parser in parsers:
            parser.__regex__ = re.compile(self.compile_regex(parser.__regex__))
        self.parsers = parsers

    def parse(self, head, baseurl, content):

        if "text/html" in head['content-type']:

            for parser in self.parsers:
                # print "checking from hrer"

                if parser.__regex__.match(baseurl):
                    # print "calling the process method"
                    parser.__process__(baseurl, content)
                    # print "after the process method"
            data = etree.HTML(content)

            for url in data.xpath('//a/@href'):
                url = urldefrag(urljoin(baseurl, url.strip()))[0]
                if self.url_pattern.match(url):
                    yield url

    def compile_regex(self, regex):
        print type(regex)
        print regex
        regex = re.escape(regex)
        regex = regex.replace("NUM", "[0-9]+")
        regex = regex.replace("ALPHA", "[a-zA-Z]+")
        regex = regex.replace("ALPHANUM", "[0-9a-zA-Z]+")
        regex = regex.replace("ANY", ".+")
        return regex
            # parser.__regex__=re.compile(parser.__regex__)
