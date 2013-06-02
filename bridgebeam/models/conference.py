from bridgebeam.models.twilio_client import twilio
from bridgebeam.models.db import DB
import logging
import re
import uuid

def remove_from_conferences(call_sid):
    db = DB()
    db.remove_call(call_sid)

def get_conferences():
    db = DB()
    return db.get_conferences()

class Conference(object):
    """This object describes a conference bridge
       and implements behavior."""

    def __init__(self, **kwargs):
        """Create identity of the conference"""
        # create our connection now, we will need it
        self.db = DB()
        # instantiate logger
        self.log = logging.getLogger('bridgebeam')
        # set identifying fields
        self.uuid = kwargs.get('uuid')
        if self.uuid == None:
            self.uuid = str(uuid.uuid4())
        try:
            # set name if it was passed as an kwarg
            self.name = self._sanitize_name(kwargs.get('name'))
        except TypeError as e:
            # otherwise, lets grab it from the database
            self.log.error(e)
            self.name = self.db.get_conference_name(self.uuid)
        # add conference to db if it doesn't already exist
        if self.uuid and self.name:
            existing_uuid = self.db.get_conference_uuid(self.name)
            if existing_uuid:
                # if it does exist, set our uuid to be equivalent
                self.uuid = existing_uuid
            else:
                self.db.create_conference(self.uuid, self.name)

    def _sanitize_name(self, name):
        """Remove all but alphanumeric characters and whitespace"""
        only_words_white = ''.join(i for i in name if re.match(r'[\w\s\-]', i))
        if len(only_words_white) >= 1:
            return only_words_white
        else:
            return None

    def _e164_number(self, number):
        only_numbers = ''.join(i for i in number if i.isdigit())
        if len(only_numbers) == 10:
            return '+1{}'.format(only_numbers)
        elif len(only_numbers) > 10:
            return '+{}'.format(only_numbers)
        else:
            return None

    def call_out(self, phone_number=None):
        """Starts twilio call with callback urls"""
        if self.uuid and phone_number:
            e164_number = self._e164_number(phone_number)
            self.log.debug("making call to twilio for: {}".format(e164_number))
            our_number = '+16502654910'
            url_to_join = "http://somedomain.com/twiml/join/{}".format(self.uuid)
            url_to_quit = "http://somedomain.com/twiml/quit"
            twilio_call  = twilio.calls.create(to=e164_number,
                                               from_=our_number,
                                               url=url_to_join,
                                               status_callback=url_to_quit)

    def add(self, call_sid=None, call_number=None):
        if call_sid and call_number and self.uuid:
            self.db.add_to_conference(call_sid, self.uuid, call_number) 

    def get_name(self):
        name = self.db.get_conference_name(self.uuid)
        return name
   
    def destroy(self):
        # close our connection to the DB
        self.db.destroy()
