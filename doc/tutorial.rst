.. _intro-tutorial:

=================
Dragline Tutorial
=================

In this tutorial, we'll assume that Dragline is already installed on your system.
If that's not the case, see :ref:`intro-install`.

We are going to use `Open directory project (FilmFare) <http://www.filmfare.com/>`_ as
our example domain to scrape.

This tutorial will walk you through these tasks:

1. Creating a new Dragline project

2. Writing a Spider to crawl a site and extract titles
   


Dragline is written in Python_. If you're new to the language you might want to
start by getting an idea of what the language is like, to get the most out of
Dragline.  If you're already familiar with other languages, and want to learn
Python quickly, we recommend `Learn Python The Hard Way`_.  If you're new to programming
and want to start with Python, take a look at `this list of Python resources
for non-programmers`_.

.. _Python: http://www.python.org
.. _this list of Python resources for non-programmers: http://wiki.python.org/moin/BeginnersGuide/NonProgrammers
.. _Learn Python The Hard Way: http://learnpythonthehardway.org/book/

Creating a project
==================

Before you start scraping, you will have set up a new Dragline project. Enter a
directory where you'd like to store your code and then run::

   dragline-init tutorial

This will create a ``tutorial`` directory with the following contents::

   tutorial/
        main.py
        settings.py


These are basically:

* ``settings.py``: the project's settings file.
* ``main.py``: file where you write your spider

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
``main.py`` under the ``tutorial`` directory::

    from dragline.htmlparser import HtmlParser
    from dragline.http import Request



    class Spider:

        def __init__(self, conf):
            self._name = "BoxOffice"
            self._start = Request("http://www.boxofficeindia.co.in/weekly-collections-%E2%80%93-box-office/")
            self._allowed_urls_regex = "http://www.boxofficeindia.co.in/weekly-collections-%E2%80%93-box-office/"

        def parse(self, response):
            data = HtmlParser(response)
            date_xpath = '//div[@id="collections-form"]/form/select/option/text()'
            for i in data.xpath(date_xpath):
                yield Request(response.url, "POST", "parse_page", form_data={'date_of_display': i})

        def parse_page(self, response):
            data = HtmlParser(response)
            title = data.xpath('//*[@id="week-date-compare"]/text()')
            if title:
                print '-' * 100, '\n', title[0]

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





