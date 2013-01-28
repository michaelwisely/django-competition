====================
 django-competition
====================

.. image:: https://travis-ci.org/michaelwisely/django-competition.png
  :target: https://travis-ci.org/michaelwisely/django-competition
  :alt: Build Status

This is a (hopefully) reusable Django_ application for hosting various
competitions. It's being developed to help run MegaMinerAI_, an
artificial intelligence programming competition held every semester at
`Missouri S&T`_. MegaMinerAI is put on by the Missouri S&T ACM
SIG-Game Developers. Check out their `github page`_!

.. _Django: https://www.djangoproject.com
.. _MegaMinerAI: http://megaminerai.com
.. _`Missouri S&T`: http://mst.edu
.. _`github page`: http://siggame.github.com


Developing
==========

Buildout
--------

This repository contains a buildout_ environment to make it easy to get
started developing.

To make things even easier, all you have to do after cloning the repo,
is run ``make``. This will pull down ``bootstrap.py`` and any other
dependencies that you may need to make sure django-competition works.

.. _buildout: http://www.buildout.org


Source
------

All of the source for the competition app is in src/competition. The
project/ directory is just a dummy project which has competition
installed as an app. This project allows us to run development
servers, unit tests... all the wonderful things that ``manage.py``
provides.


