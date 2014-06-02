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

    def __init__(self, url, method="GET", form_data=None, headers={}, callback=None, meta=None,):
        """
            :param url: the URL of this request
            :type url: string
            :param method: the HTTP method of this request. Defaults to ``'GET'``.
            :type method: string
            :param headers: the headers of this request.
            :type headers: dict
            :param callback: name of the function to call after url is downloaded.
            :type callback: string
            :param meta:  A dict that contains arbitrary metadata for this request.
            :type meta: dict
        """
        self.method = method
        self.url = url
        self.callback = callback
        self.meta = meta
        self.form_data = form_data
        self.HEADERS.update(headers)

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

        >>> req = Request("http://www.example.org")
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
            res = Response(self.url, content, headers, self.meta)
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

    def __init__(self, url=None, body=None, headers=None, meta=None):
        if url:
            self.url = url
        if body:
            self.body = body
        if headers:
            self.headers = headers
        if meta:
            self.meta = meta
