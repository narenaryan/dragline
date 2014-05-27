import httplib2
from urllib import urlencode
import socket
from hashlib import sha1
import collections

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

    def get_unique_id(self):
        formdata =  urlencode({i: j for i,j in  sorted(self.form_data.items(),key =lambda t: t[0])})
        str = self.method+":"+self.url+":"+formdata
        return self.usha1(str)


