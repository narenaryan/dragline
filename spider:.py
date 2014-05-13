from lxml import etree


class FilmFareSpider:
   

    def __init__(self):
        self.http = httplib2.Http(timeout=350)
        self._start_url="http://www.filmfare.com/reviews/"
        self._allowed_url_pattern="http://www.filmfare.com/reviews/"
        pass


    def parse(self,baseurl,data):
        data=etree.HTML(data)
        url_xp="//figure[@class='featured']"

        for url in data.xpath(url_xp+'//a/@href'):
            url = urldefrag(urljoin(baseurl, url.strip()))[0]
            

            url_info={}
            url_info['baseurl']=url
            
            url_info['callback']="parse_review"

            yield url_info


        for url in data.xpath('//div[@class="pageNav"]//a/@href'):
            url = urldefrag(urljoin(baseurl, url.strip()))[0]
           

            url_info={}
            url_info['baseurl']=url
            
            url_info['callback']="parse_review"

            yield url_info







            #push to quee
            #self.parse_review(self,url,content)


    def parse_review(self,baseurl,data):
        data=etree.HTML(data)
        title=data.xpath("//div[@class='TopPart']/h1/text()")
        if title:
            print title


            










        

