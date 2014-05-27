import httplib2
from urllib import urlencode
import socket


class RequestError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Request:
    retry = 0

    def __init__(self, url, method="GET", callback=None, meta=None, form_data=None):
        self.method = method
        self.url = url
        self.callback = callback
        self.meta = meta
        self.form_data = form_data
        self.http = httplib2.Http()

    def send(self):
        if self.form_data:
            self.form_data = urlencode(self.form_data)
        try:
            response, content = self.http.request(self.url, self.method, self.form_data)
        except (httplib2.ServerNotFoundError, socket.timeout, socket.gaierror) as e:
            self.retry += 1
            raise RequestError(e.message)
        if self.callback:
            if self.meta:
                self.callback(response, content, self.meta)
            else:
                self.callback(response, content)
        return response, content
