====
BridgeBeam
====
What is it?
===========
BridgeBeam is a Python application built around Bottle that has four distinct endpoints.
1. /
   - This is the home page that you use to control BridgeBeam (a.k.a webui)
2. /api/v1/
   - These are the resources being hit by the AJAX client on the webui or other services
3. /twiml/
   - These resources are in twiml format made specically for Twilio callbacks 
     

How do I use it?
================
To start, you will want to install the module:
$ python setup.py install
