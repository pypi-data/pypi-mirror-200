====================
sphinxcontrib-oembed
====================

Embed HTML content by URL from eEmbed consumer

.. caution:: DEPRECATED

   This extension is stopped developmnent.
   `oEmbedPy <https://pypi.org/project/oEmbedPy>`_ contains same features of it and is more useful.

   Please use oEmbedPy instead.

Overview
========

This is Sphinx extension to provide easy embed some third-party websites content.

Example for embed tweet from Twitter:

* In defaults, you use ``raw`` directive, get and paste blockquuote and script tags from Twitter Publish.
* With this, you use ``oembed`` and paste tweet URL only!

Installation
============

This is registered in PyPI.

.. code-block:: console

   pip install sphinxcontrib-oembed

Usage
=====

Add this extension into your ``conf.py`` of Sphinx.

.. code-block:: python

   extensions = [
       "sphinxcontrib.oembed",
   ]

   # You can change User-agent
   # Default is sphinxcontrib-oembed/{ext-version}
   obmed_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"

Changes
=======

v0.2.1
------

* Published on PyPI

v0.2.0
------

* Enable to confiugre User-agent when request oEmbed providers

License
=======

Apache-2.0
