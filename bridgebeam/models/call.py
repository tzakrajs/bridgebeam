from bridgebeam import twilio
import logging
import uuid
from bridgebeam.models.db import DB

class Call(object):
    """This object maintains state about an individual Twilio call and
       provides methods to manipulate the call.

    """
    
    def __init__(self, **kwargs):
        """The logical representation of a call between bridgebeam and the user.

        Keyword Arguments:
          - phone_number: the E.164 formatted number
          - conference_name: the friendly name for the conference
          - sid: an existing twilio call_sid
        """
        #setup logger
	self.log = logging.getLogger('bridgebeam')
        #set call sid manually
        self.sid = kwargs.get('sid')
        conference_name = kwargs.get('conference_name')
        #create twilio call and set sid automatically
        phone_number = kwargs.get('phone_number')
        if phone_number != None:
            self.log.debug("making call to twilio for: {}".format(phone_number))
            our_number = '+16502654910'
            url_to_join = "http://somedomain.com/twiml/join"
            url_to_quit = "http://somedomain.com/twiml/quit"
            twilio_call  = twilio.calls.create(to=phone_number,
                                               from_=our_number,
                                               url=url_to_join,
                                               status_callback=url_to_quit)
            self.sid = self.twilio_call.sid
        else:
            self.log.error("fail boat when trying to call {}".format(phone_number))

    def get_status(self):
        twilio_call = twilio.calls.get(self.sid)
        return twilio_call.status

    def disconnect(self):
        twilio.calls.hangup(self.sid)
