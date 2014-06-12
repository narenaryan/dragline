htmlparser Module
=========================

Basic parser module for extracting content from html data,
there is a main function in htmlparser called as HtmlParser. 
Apart from entire Dragline,htmlparser alone is a powerful parsing application.

HtmlParser Function
-------------------

.. automodule:: dragline.htmlparser
    :members: HtmlParser


lxml Element object
-------------------
lxml Element object is returned by the HtmlParser function.

The two parsing methods of the lxml Element object are:
    * `extract_urls`_
    * `extract_text`_


extract_urls
------------
This function fetches all the links from the webpage in response by 
the specified xpath as its argument.

If xpath is not included then links are fetched from entire document.
From previous example let lxml Element be
parse_obj.
   
    >>> parse_obj.extract_urls('//div[@class="product"]')

will fetch you all the links from the div tag of html where class is 'product'

extract_text
------------
This function grabs all the text from the web page that specified.xpath is an optional
argument.If specified the text obtained will  be committed to condition in xpath expression.

    >>> parse_obj.extract_text('//html')


1.Locating an element in a webpage
----------------------------------
we can locate element from a webpage using two following inbuilt methods for lxml Element object.
they are:

    * Locating by XPath
    * Locating by CSS selector

1.1.Locating by XPath
---------------------
XPath is the language used for locating nodes in an XML document. As HTML can be an implementation of XML (XHTML),Dragline users can leverage this powerful language to target elements in their web applications. XPath extends beyond (as well as supporting) the simple methods of locating by id or name attributes, and opens up all sorts of new possibilities such as locating the third checkbox on the page.

One of the main reasons for using XPath is when you don’t have a suitable id or name attribute for the element you wish to locate. You can use XPath to either locate the element in absolute terms (not advised), or relative to an element that does have an id or name attribute. XPath locators can also be used to specify elements via attributes other than id and name.

For instance if we want to fetch links from::

    <html>
        <head>
        </head>
        <body>
            <div class="tree">
                <a href="http://www.treesforthefuture.org/">Botany</a>
            </div>
            <div class="animal">
                <a href="http://www.animalplanet.com/">Zoology</a>
            </div>
        </body>
    </html>


then we can use the following XPath expressions.
    
    >>> parse_object.extract_url('//div[@class="tree"]')

it fetches links only from tree class division.

    >>> parse_object.extract_text('//div[@class="animal"]')

it grabs text from div tag whose class name was animal 

1.2.Locating by CSS selector
----------------------------
Use this when you want to locate an element by CSS selector syntaxt. With this strategy, the first element with 
the matching CSS selector will be returned.lxml Element object has a method for fetching dom elements from CSS selecor
path,it is illustrated below.::

    <html>
         <body>
              <p class="content">
              This is content of paragraph.and it contains a link
              <a href="www.gutenberg.com></a>
              </p>
        </body>
    <html>

css
---
css is the function to retrieve the elements of html.It fetches the DOM elemnts according to
the CSS selector expression specified as argument.
So for above HTML we can access the content in paragraph as

    >>> print parse_object.css('p.content')

w3 schools have good documentation on the on CSS Selectors 
    http://www.w3schools.com/css/css_selectors.asp.

2.Other methods
---------------
lxml Element object has the other useful methods which are inherited from its predecessors.

2.1.xpath()
-----------
This function directly accumulate the results from the xpath expression.It is used to fetch
the html body elements directly. 

    >>> print parse_obj.xpath('//div[@class="mw-content-ltr"]')


2.2.find()
----------
This function returns the first matched tag of the xpath expression given to the statement.
xpath notation here used is ElementPath.So include '.' in front of the xpath expression.

    >>> print parse_object.find('.//div').tag

this matches the first div tag in the response html body.

2.3.findall()
-------------
This function returns the list of all matched tags with the given expression.

    >>> mylist=parse_object.findall('.//a')


