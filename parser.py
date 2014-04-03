import re
from html import lxml

class Parser:
	def __init__(self,allowed_urls):
		self.url_pattern=re.compile('(%s)'%'|'.join(re.escape(allowed_urls)))

	def parse(self,baseurl,content):
		data = html.fromstring(content)
        for url in data.xpath('//a/@href'):
            url = urldefrag(urljoin(baseurl, url.strip()))[0]
            if self.url_pattern.match(url):
                yield url

