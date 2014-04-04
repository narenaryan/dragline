import re


from urlparse import urljoin, urldefrag


class Parser:

    def __init__(self, allowed_urls, parsers):
        self.url_pattern = re.compile(
            '(%s)' % '|'.join(re.escape(i) for i in allowed_urls))
        self.parsers=parsers

    def parse(self, head, baseurl, content):
        #print baseurl
        if "text/html" in head['content-type']:
            

            for parser in self.parsers:
                
                if re.match(re.escape(parser.__regex__),baseurl):
                    parser.__process__(baseurl,content)

            for url in data.xpath('//a/@href'):
                url = urldefrag(urljoin(baseurl, url.strip()))[0]
                if self.url_pattern.match(url):
                    yield url

    