.. _parser:

=========================
htmlparser Module
=========================

Basic parser module for extracting content from html data,
there is a main function in htmlparser called as HtmlParser. 
Apart from entire Dragline,htmlparser alone is a powerful parsing application.

HtmlParser Function
-------------------

.. autofunction:: dragline.htmlparser.HtmlParser


 lxml.html.HtmlElement object

HtmlElement object is returned by the HtmlParser function::
    
    >>>req=Request('www.gutenberg.com')
    >>>parse_object=HtmlParser(req.send())

The parsing methods of the modified lxml HtmlElement object are:
    * `xpath`_
    * `css`_
    * `extract_urls`_
    * `extract_text`_
    * `find`_
    * `findall`_


.. method:: xpath(expression)

This function directly accumulate the results from the xpath expression.It is used to fetch
the html body elements directly::

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
    
    >>> parse_object.extract_urls('//div[@class="tree"]')
    
        http://www.treesforthefuture.org/

it fetches links only from tree class division.

    >>> parse_object.extract_text('//div[@class="animal"]')
    
        Zoology

it grabs text from div tag whose class name was animal 



.. method:: css(cssselector)

css is the function to retrieve the elements of html.It fetches the DOM elemnts according to
the CSS selector expression specified as argument::

    <html>
        <body>
            <p class="content">
            This is content of this paragraph.and it contains a link
            <a href="www.gutenberg.com></a>
            </p>
        </body>
    <html>

So for above HTML we can access the content in paragraph as

    >>> print parse_object.css('p.content')

        This is contents of this paragraph.and it contains a link.

w3 schools have good documentation on the on CSS Selectors 
    http://www.w3schools.com/css/css_selectors.asp.

.. method:: extract_urls(xpath_expr)

This function fetches all the links from the webpage in response by 
the specified xpath as its argument.

If xpath is not included then links are fetched from entire document.
From previous example let HtmlElement be
parse_obj.
   
    >>> parse_obj.extract_urls('//div[@class="product"]')

will fetch you all the links from the div tag of html where class is 'product'

.. method:: extract_text(xpath_expr)

This function grabs all the text from the web page that specified.xpath is an optional
argument.If specified the text obtained will  be committed to condition in xpath expression.

    >>> parse_obj.extract_text('//html')



.. method:: find(ElementPath)

This function returns the first matched tag of the xpath expression given to the statement.
xpath notation here used is ElementPath.So include '.' in front of the xpath expression.

    >>> print parse_object.find('.//div').tag

this matches the first div tag in the response html body.

.. method:: findall(ElementPath)

This function returns the list of all matched tags with the given expression.

    >>> mylist=parse_object.findall('.//a')


