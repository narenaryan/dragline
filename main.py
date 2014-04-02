import httplib2
import httpcache2
import sys
import os

http = httplib2.Http()


def process_url(url):
    head, content = http.request(url, 'GET')
    print head



if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.path.insert(0, sys.argv[1])
        import main
        print main.START_URL