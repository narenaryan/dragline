import httplib2
from urllib import urlencode
import socket
from hashlib import sha1


class RequestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Request:
    retry = 0
    delay = 0.5
    min_delay = 0.5
    max_delay = 60
    headers = {
        "accept": "text/html",
        'content-type': "application/x-www-form-urlencoded"
    }

    def __init__(self, url, method="GET", callback=None, meta=None, form_data=None, headers=None):
        self.method = method
        self.url = url
        self.callback = callback
        self.meta = meta
        self.form_data = form_data
        if headers is not None:
            self.headers = headers
        self.http = httplib2.Http()

    def __str__(self):
        return self.get_unique_id(False)

    def usha1(self, x):
        """sha1 with unicode support"""
        if isinstance(x, unicode):
            return sha1(x.encode('utf-8')).hexdigest()
        else:
            return sha1(x).hexdigest()

    def send(self):
        if self.form_data:
            self.form_data = urlencode(self.form_data)
        try:
            response, content = self.http.request(
                self.url, self.method, self.form_data, self.headers)
            response['url'] = self.url
        except (httplib2.ServerNotFoundError, socket.timeout, socket.gaierror) as e:
            self.retry += 1
            raise RequestError(e.message)
        return response, content

    def get_unique_id(self, hashing=True):
        request = self.method + ":" + self.url
        if self.form_data:
            request += ":" + urlencode(
                {i: j for i, j in sorted(self.form_data.items(),
                                         key=lambda t: t[0])})
        if hashing:
            return self.usha1(request)
        else:
            return request

    @classmethod
    def updatedelay(cls, end, start):
        delay = end - start
        cls.delay = min(max(cls.min_delay, delay, (cls.delay + delay) / 2.0), cls.max_delay)
