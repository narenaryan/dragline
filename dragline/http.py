from urllib import urlencode
import socket
from hashlib import sha1
import time
import httplib2
from defaultsettings import RequestSettings


class RequestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Request(RequestSettings):

    def __init__(self, url, method="GET", callback=None, meta=None, form_data=None, headers=None):
        self.method = method
        self.url = url
        self.callback = callback
        self.meta = meta
        self.form_data = form_data
        if headers is not None:
            self.HEADERS = headers

    def __str__(self):
        return self.get_unique_id(False)

    def usha1(self, x):
        """sha1 with unicode support"""
        if isinstance(x, unicode):
            return sha1(x.encode('utf-8')).hexdigest()
        else:
            return sha1(x).hexdigest()

    def send(self):
        """
        This function sends HTTP requests.

        :returns: response
        :rtype: :class:`Response`
        :raises: :exc:`RequestError`: when failed to fetch contents

        >>> req = Request("http://www.example.org",method="GET", callback="parse", meta=dict(a=1,b=2))
        >>> response = req.send()
        >>> print response.headers['status']
        200

        """
        form_data = urlencode(self.form_data) if self.form_data else None
        try:
            time.sleep(self.DELAY)
            start = time.time()
            http = httplib2.Http()
            headers, content = http.request(
                self.url, self.method, form_data, self.HEADERS)
            res = Response(self.url, content, headers)
            end = time.time()
            self.updatedelay(end, start)
        except (httplib2.ServerNotFoundError, socket.timeout, socket.gaierror) as e:
            raise RequestError(e.message)
        return res

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
        cls.DELAY = min(
            max(cls.MIN_DELAY, delay, (cls.DELAY + delay) / 2.0), cls.MAX_DELAY)


class Response:

    def __init__(self, url=None, body=None, headers=None):
        if url:
            self.url = url
        if body:
            self.body = body
        if headers:
            self.headers = headers
