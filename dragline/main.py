from gevent import monkey, spawn, joinall
monkey.patch_all()

import sys
import argparse
import os
import traceback
import logging
from crawl import Crawler

logging.basicConfig()


def load_module(path, filename):
    try:
        sys.path.insert(0, path)
        module = __import__(filename)
        del sys.path[0]
        return module
    except Exception as e:
        logging.exception("Failed to load module %s" % filename)
        raise ImportError


def main(abs_name):
    path, filename = os.path.split(abs_name)
    module = load_module(path, filename.strip('.py'))
    spider = getattr(module, module.spider_class)()
    Crawler.load_spider(spider)
    crawlers = [Crawler() for i in xrange(5)]
    joinall([spawn(crawler.process_url) for crawler in crawlers])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help='spider file name')
    args = parser.parse_args()
    filename = os.path.abspath(args.spider)
    main(filename)
