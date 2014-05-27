from dragline.htmlparser import HtmlParser


class Spider:

    def __init__(self, conf):
        self._name = "Test_BoxOffice"
        self._start = {"url": "http://www.boxofficeindia.co.in/weekly-collections-%E2%80%93-box-office/"}
        self._allowed_urls_regex = "http://www.boxofficeindia.co.in/weekly-collections-%E2%80%93-box-office/"

    def parse(self, response, data):
        data = HtmlParser(response['url'], data)
        date_xpath = '//div[@id="collections-form"]/form/select/option/text()'
        url_info = {"method": "POST", "url":
                    response['url'], "callback": "parse_page"}
        for i in data.extract(date_xpath):
            url_info['form-data'] = {'date_of_display': i}
            yield url_info

    def parse_page(self, response, data):
        data = HtmlParser(response['url'], data)
        title = data.extract('//*[@id="week-date-compare"]/text()')
        if title:
            print '-' * 100, '\n', title[0]
