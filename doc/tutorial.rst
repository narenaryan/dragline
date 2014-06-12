.. _intro-tutorial:

=================
Dragline Tutorial
=================

Beginning instructions
-----------------------
Dragline is entirely written in python.It facilitates to create the different spiders upon
the stack of the performance,robustness and easieness.The most engaging issue with Dragline 
is the creation of custom spiders using one central crawler that availale in the Dragline library.

Let us build a spider to crawl entire python docs section and collect URL followed by storing.
The work of redis backend will be abstracted 
In this tutorial, we'll assume that Dragline is already installed on your system.
If that's not the case, see :ref:`intro-install`.Also See the additonal reqiurements.

In this tutorial we are going to build custom spider,this is a single illustration.But
Dragline encapsulate much power in its functionality.First task of the Dragline is to provide
a common framework to build  different spiders.

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
Let us think our spider name is pydocs.

Before you start scraping, you will have to set up a new Dragline project. Traverse into a
directory where you'd like to store your spider and its associated code and then run the following command::

   dragline-init pydocs

If you are a django developer then you might be familiar with above type of command.

This will create a ``pydocs`` directory with the following two files::

      pydocs/
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
``main.py`` under the ``pydocs`` directory::

  from dragline.htmlparser import HtmlParser
  from dragline.http import Request


  class Spider:

      def __init__(self, conf):
          self._name = "pydocs"
          self._start = Request("https://docs.python.org/3/")
          self._allowed_urls_regex = ".*"
          self.conf = conf

      def parse(self, response):
          html = HtmlParser(response)
          table = html.find('.//table')
          for url in table.extract_urls():
              yield Request(url, callback="parse_group")

      def parse_group(self, response):
          html = HtmlParser(response)
          for i in html.extract_urls('//a[@class="reference internal"]'):
              yield Request(i, callback="parse_page")

      def parse_page(self, response):
          html = HtmlParser(response)
          page = {
              'title': 'strip(//h1)',
              'subtitles': ['strip(//h2)']
          }
          print html.extract(page)

Crawling
--------

To put our spider to work, go to the project's top level directory and run::

   dragline .

The ``dragline .`` command runs the spider for the ``filmfare.com`` domain. You
will get an output similar to this::

    .........
    2014-06-12 14:57:30,492 [INFO] dragline: Processing GET:https://docs.python.org/3/reference/import.html
    {'subtitles': [u'4.1. Getting and Installing MacPython\xb6',
                  u'4.2. The IDE\xb6',
                  u'4.3. Installing Additional Python Packages\xb6',
                  u'4.4. GUI Programming on the Mac\xb6',
                  u'4.5. Distributing Python Applications on the Mac\xb6',
                  u'4.6. Other Resources\xb6'],
    'title': u'4. Using Python on a Macintosh\xb6'}
    2014-06-12 14:57:30,781 [INFO] dragline: Finished processing GET:https://docs.python.org/3/using/mac.html
    2014-06-12 14:57:30,781 [INFO] dragline: Processing GET:https://docs.python.org/3/reference/datamodel.html
    {'subtitles': [u'5.1. pyvenv - Creating virtual environments\xb6'],
    'title': u'5. Additional Tools and Scripts\xb6'}
    2014-06-12 14:57:32,312 [INFO] dragline: Finished processing GET:https://docs.python.org/3/using/scripts.html
    2014-06-12 14:57:32,313 [INFO] dragline: Processing GET:https://docs.python.org/3/reference/compound_stmts.html
    {'subtitles': [u'3.1. Installing Python\xb6',
                  u'3.2. Alternative bundles\xb6',
                  u'3.3. Configuring Python\xb6',
                  u'3.4. Python Launcher for Windows\xb6',
                  u'3.5. Additional modules\xb6',
                  u'3.6. Compiling Python on Windows\xb6',
                  u'3.7. Other resources\xb6'],
    'title': u'3. Using Python on Windows\xb6'}
    2014-06-12 14:57:33,267 [INFO] dragline: Finished processing GET:https://docs.python.org/3/using/windows.html
    {'subtitles': [u'1.1. Command line\xb6', u'1.2. Environment variables\xb6'],
    'title': u'1. Command line and environment\xb6'}
    2014-06-12 14:57:33,283 [INFO] dragline: Finished processing GET:https://docs.python.org/3/using/cmdline.html
    2014-06-12 14:57:33,283 [INFO] dragline: Processing GET:https://docs.python.org/3/reference/introduction.html
    2014-06-12 14:57:33,284 [INFO] dragline: Processing GET:https://docs.python.org/3/reference/grammar.html
    {'subtitles': [u'3.1. Objects, values and types\xb6',
                  u'3.2. The standard type hierarchy\xb6',
                  u'3.3. Special method names\xb6'],
    'title': u'3. Data model\xb6'}
    2014-06-12 14:57:34,926 [INFO] dragline: Finished processing GET:https://docs.python.org/3/reference/datamodel.html


