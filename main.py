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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help='spider file name')
    args = parser.parse_args()
    path, filename = os.path.split(os.path.abspath(args.spider))
    module = load_module(path, filename.strip('.py'))
    spider = getattr(module, module.spider_class)()
    Crawler.load_spider(spider)
    print spider

if __name__ == "__main__":
    main()
    #try:
        #main()
    #except:
        #pass
