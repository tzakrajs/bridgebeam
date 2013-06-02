#!/usr/bin/env python
import os
import sys

# do some magic if we are running wsgi
try:
    import mod_wsgi

    # Change working directory so relative paths (and template lookup) work again
    os.chdir(os.path.dirname(__file__))

    # Add working directory to paths
    sys.path.append(os.path.dirname(__file__))
except:
    pass

from bridgebeam import application
import logging

# config log format
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-21s %(levelname)s %(name)s (%(funcName)-s) %(process)d:%(thread)d - %(message)s',
                    filename='lol.log')

# global variables config
application.config.Twiml.callback_base_url = 'http://somedomain.com:8080'
application.config.Twilio.account_sid = 'ACCOUNT_SID'
application.config.Twilio.auth_token = 'AUTH_TOKEN'
application.config.DB.path = './bridgebeam.db'

# setup the bridgebeam server
from bridgebeam.controllers import *

# start the bottle server if we aren't running as wsgi

try:
    import mod_wsgi
    pass
except:
    application.run(host='0.0.0.0', port=8080)
