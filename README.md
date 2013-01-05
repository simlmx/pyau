pyau
====

Python Audio Unit Host

I don't work much on this projet anymore, but don't hesitate to email me for any questions/comments/etc.



Current features
================

* Hosts audio units
* Supports multiple tracks
* Can use midi files to bounce audio
* Listens to incoming midi messages (e.g. from a keyboard)
* ~~Ugly generic gui for audio units~~ Disabled because buggy...


Requirements
============
A mac with at least Leopard (10.5) with the following installed

* Python 2.5 or higher (with pip)
* Xcode
* Swig (with python bindings)


Installation
============

    git clone https://github.com/simlmx/pyau.git
    cd pyau
    python setup.py build  # Make sure you don't skip this step!
    python setup.py install

In the python interpreter (opened from a different directory), verify that the following works:

    import pyau


Usage
=====
* You can find a basic example in pyau/example.py
Note


TODOs
================
* Loading of carbon/cocoa audio units' gui


