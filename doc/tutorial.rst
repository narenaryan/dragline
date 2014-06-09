.. _intro-tutorial:

=================
Dragline Tutorial
=================

Become a Spider man 
-------------------
Yes,you heared it right.Dragline really creates spiders in a lightening speed for you.This tutorial
illustrates how it is possible.

Let us build a spider to crawl entire python docs section and collect URL.
In this tutorial, we'll assume that Dragline is already installed on your system.
If that's not the case, see :ref:`intro-install`.Also See the additonal reqiurements.

In this tutorial we are going to build custom spider,ones spider will be different 
from others but Dragline provides a common framework to build  different spiders.

We are going to use `Open directory project (Python Docs) <https://docs.python.org/3/>`_ as
our example domain to crawl.

This tutorial will walk you through these tasks:

1. Creating a new Dragline project.

2. Writing a Spider to crawl a site and extract titles.
   
3. A thorough understanding of Dragline API.

Dragline is toally designed in Python2.7 .You are here because you are a python developer. If not don't be panic.Heartly welcome to python,and want to learn
Python quickly, we recommend `Learn Python The Hard Way`_.  If you're new to programming
and want to start with Python, take a look at `this list of Python resources
for non-programmers`_.

.. _Python: http://www.python.org
.. _this list of Python resources for non-programmers: http://wiki.python.org/moin/BeginnersGuide/NonProgrammers
.. _Learn Python The Hard Way: http://learnpythonthehardway.org/book/

Creating a project
==================
Let us think our spider name is docspider.

Before you start scraping, you will have to set up a new Dragline project. Traverse into a
directory where you'd like to store your spider and its associated code and then run the following command::

   dragline-init docspider

If you are a django developer then you might be familiar with above type of command.

This will create a ``docspider`` directory with the following two files::

   docspider/
        main.py
        settings.py


These are basically:

* ``settings.py``: the project's settings file.
* ``main.py``: file where we write our custom spider

Our first Spider
================

Spiders are user-written classes used to scrape information from a domain (or group
of domains).

They define an initial list of URLs to download, how to follow links, and how
to parse the contents of those pages to extract content.

To create a Spider, you must create a class named Spider in main.py
define the three main, mandatory, attributes:

* :attr:`~Spider._name`: identifies the Spider. It must be
  unique, that is, you can't set the same name for different Spiders.

* :attr:`~Spider._start_url`: is a list of URLs where the
  Spider will begin to crawl from.  So, the first pages downloaded will be those
  listed here. The subsequent URLs will be generated successively from data
  contained in the start URLs.
* :attr:`~Spider._allowed_urls_regex`: is a regex of the allowed urls through which the spider will move

* :meth:`~Spider.parse` is a method of the spider, which will
  be called with the downloaded :class:`Response` object of each
  start URL. The response is passed to the method as the first and only
  argument.

  This method is responsible for parsing the response data and extracting
  scraped data and more URLs to follow.



This is the code for our first Spider; save it in a file named
``main.py`` under the ``docspider`` directory::

    from dragline.htmlparser import HtmlParser
    from dragline.http import Request


    class Spider:

        def __init__(self, conf):
            self._name = "FilmFare"
            self._start = Request("http://www.filmfare.com/reviews/")
            self._allowed_urls_regex = "http://www.filmfare.com/reviews/"
            self.conf = conf

        def parse(self, response):
            data = HtmlParser(response)
            url_xp = "//figure[@class='featured']"
            for url in data.extract_urls(url_xp):
                yield Request(url=url, callback="parse_review")

            for url in data.extract_urls('//div[@class="pageNav"]'):
                yield Request(url=url, callback="parse")

        def parse_review(self, response):
            data = HtmlParser(response)
            title = data.xpath("//div[@class='TopPart']/h1/text()")
            if title:
                print title

Crawling
--------

To put our spider to work, go to the project's top level directory and run::

   dragline .

The ``dragline .`` command runs the spider for the ``filmfare.com`` domain. You
will get an output similar to this::

    2014-05-30 12:28:48,840 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/
    2014-05-30 12:28:49,866 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-raanjhanaa-3492.html
    2014-05-30 12:28:49,867 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-fukrey-3429.html
    2014-05-30 12:28:49,869 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-man-of-steel-3430.html
    2014-05-30 12:28:49,870 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/music-review-ghanchakkar-3512.html
    2014-05-30 12:28:49,882 [INFO] dragline: Finished processing GET:http://www.filmfare.com/reviews/
    2014-05-30 12:28:49,883 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-kochadaiiyaan-6217.html
    ['Movie Review: Raanjhanaa']
    2014-05-30 12:28:50,622 [INFO] dragline: Finished processing GET:http://www.filmfare.com/reviews/movie-review-raanjhanaa-3492.html
    ['Movie Review: Fukrey']
    2014-05-30 12:28:50,628 [INFO] dragline: Finished processing GET:http://www.filmfare.com/reviews/movie-review-fukrey-3429.html
    ['Music Review: Ghanchakkar']
    2014-05-30 12:28:50,633 [INFO] dragline: Finished processing GET:http://www.filmfare.com/reviews/music-review-ghanchakkar-3512.html
    2014-05-30 12:28:50,634 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-heropanti-6216.html
    ['Movie Review: Man Of Steel']
    2014-05-30 12:28:50,639 [INFO] dragline: Finished processing GET:http://www.filmfare.com/reviews/movie-review-man-of-steel-3430.html
    2014-05-30 12:28:50,639 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-xmen-days-of-future-past-6202.html
    2014-05-30 12:28:50,640 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-the-xpos-6154.html
    2014-05-30 12:28:50,641 [INFO] dragline: Processing GET:http://www.filmfare.com/reviews/movie-review-godzilla-6145.html
    ['Movie Review: Kochadaiiyaan']
    2014-05-30 12:28:50,818 [INFO] dragline: Finished processing GET:http://www.filmfare.com/reviews/movie-review-kochadaiiyaan-6217.html





