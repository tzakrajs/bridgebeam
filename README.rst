BridgeBeam
==========

What is it?
-----------
BridgeBeam is a Python application built around Bottle that has four distinct endpoints.

1. / This is the home page that you use to control BridgeBeam (a.k.a webui)
   
2. /api/v1/ These are the resources being hit by the AJAX client on the webui or other services

3. /twiml/ These resources are in twiml format made specically for Twilio callbacks

How do I install it?
--------------------
To start, you will want to install the module:

.. code-block:: console

    $ sudo python ./setup.py install


Then you can start the server with these commands:

.. code-block:: console

    >>> from bridgebeam import application
    >>> application.config.Twiml.callback_base_url='http://somedomain.com:8080'
    >>> application.config.Twilio.account_sid='AC3813535560204085626521'
    >>> application.config.Twilio.auth_token='2flnf5tdp7so0lmfdu3d7wod'
    >>> application.config.DB.path='/var/lib/bridgebeam/bridgebeam.db'
    >>> from bridgebeam.controllers import *
    >>> application.run(host='0.0.0.0', port=8080)
    Bottle v0.11.4 server starting up (using WSGIRefServer())...
    Listening on http://0.0.0.0:8080/
    Hit Ctrl-C to quit.


There is a working sample included named run_server.py that can also be loaded with mod_wsgi for easy deployment on your favorite web server.
