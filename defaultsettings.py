import logging

REQUEST_HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
    "accept": "text/html"
}
LOG_LEVEL = 'DEBUG'
LOGFORMATTER = logging.Formatter('%(levelname)s: %(message)s')
LOGHANDLER = logging.StreamHandler()
