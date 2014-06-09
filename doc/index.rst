.. Dragline documentation master file, created by
   sphinx-quickstart on Thu May 29 16:10:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Dragline's documentation!
====================================

What is Dragline?
=================
Dragline is not a pre-defined application to perform a single task.It is a crawler that crawls through 
any no of pages and fetches the URL.The main theme of dragline is to create your own spiders on the web.
The creative usage of the Dragline remains in the hands of the developer.This documentation leads you 
to easily come up with all the tools available and how to use them to build a custom spider in few minutes.

Yet Another Spider?
===================
There are some crawling packages available,why another one?.We strongly believe that the effieciency
matters.Dragline is different from others in many aspects.The most significant feautures are:

	1. Built from scratch.
	2. redis backend for persistant storage.
	3. used high level synchronous API through greenlets.
  

First steps
===========
.. toctree::
   :hidden:

   install
   tutorial
   
:doc:`install`
    Get Dragline installed on your computer.

:doc:`tutorial`
    Write your first Dragline project.


Contents
===========

.. toctree::
    http
    parser



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

