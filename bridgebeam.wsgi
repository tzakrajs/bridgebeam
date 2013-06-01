import logging
import os
import sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

# Add working directory to paths
sys.path.append(os.path.dirname(__file__))

# Set Twilio Account SID and Auth Token
os.environ['TWILIO_ACCOUNT_SID'] = 'ACCOUNT_SID'
os.environ['TWILIO_AUTH_TOKEN'] = 'AUTH_TOKEN'

import bottle
import bridgebeam
# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi
application = bridgebeam.app

logging.basicConfig(level=logging.DEBUG,
                             format='%(asctime)-21s %(levelname)s %(name)s (%(funcName)-s) %(process)d:%(thread)d - %(message)s',
                             filename='lol.log')
