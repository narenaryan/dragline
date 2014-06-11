from dragline import http
from dragline import htmlparser
import unittest
import data
import re
class HtmlParserTest(unittest.TestCase):
    def test_links(self):
        mybool=True
        urlpattern=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        res=http.Response('http://norvig.com/',data.hstring)
        parse_object=htmlparser.HtmlParser(res)
        for url in parse_object.links():
            if not urlpattern.match(url):
                mybool=False
                break
        self.assertTrue(mybool)
    def test_gettext(self):
    	self.assertTrue(True)
    def test_extract(self):
    	self.assertTrue(True)
    def test_cssselect(self):
        
    	self.assertTrue
    def test_css(self):
    	self.assertTrue(True)

if __name__=="main":
	unittest.main()
