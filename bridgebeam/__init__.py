__version__ = "0.1"

from bottle import Bottle, TEMPLATE_PATH
from twilio.rest import TwilioRestClient
import logging

#create bottle instance
app = Bottle()

#create twilio api client
twilio = TwilioRestClient()
TEMPLATE_PATH.append("./bridgebeam/views/")
#TEMPLATE_PATH.remove("./views/")

#load controllers
from bridgebeam.controllers import *

# python < 2.7 compatibility
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
