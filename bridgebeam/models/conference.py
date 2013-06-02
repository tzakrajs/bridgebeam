from bridgebeam.models.twilio_client import twilio
from bridgebeam.models.db import DB
import logging
import re
import uuid

class Conference(object):
    """
    Context manager used to maintain unique identifiers for conference bridges
    
    """

    def __init__(self, **kwargs):
        """Establish conference identity needed to direct new callers"""
        # instantiate logger
        self.log = logging.getLogger('bridgebeam')
        # get bridgebeam conference uuid
        self.uuid = kwargs.get('uuid', uuid.uuid4())
        # connect to the db
        self.db = DB()
        try:
            # set conference name if it was passed as an kwarg
            self.name = self._sanitize_name(kwargs.get('name'))
        except TypeError as e:
            # otherwise, lets grab it from the database
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
        """Remove all but numerals then format for E.164"""
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
            url_to_join = '{}/twiml/join/{}'.format(self.twiml_base_url, self.uuid)
            url_to_quit = '{}/twiml/quit'.format(self.twiml_base_url)
            twilio_call  = twilio.calls.create(to=e164_number,
                                               from_=our_number,
                                               url=url_to_join,
                                               status_callback=url_to_quit)

    def add(self, call_sid=None, call_number=None):
        """Associates a call to the conference"""
        if call_sid and call_number and self.uuid:
            self.db.add_to_conference(call_sid, self.uuid, call_number) 

    @classmethod
    def remove_from_conferences(call_sid):
        """Removes call from all conferences for given call_sid"""
        db = DB()
        db.remove_call(call_sid)
        db.destroy()

    def get_name(self):
        """Determines bridgebeam conference uuid"""
        name = self.db.get_conference_name(self.uuid)
        return name
   
    @classmethod
    def get_conferences(self):
        """
        Returns a dict of conferences
        - Each key in the dict contains a list of phone numbers
        - Those phone numbers represent present calls connected to the bridge

        """ 
        db = DB()
        conferences = {}
        rows = db.get_conferences()
        for conference_name, phone_number in rows:
            if conference_name in conferences.keys():
                conferences[conference_name].append(phone_number)
            else:
                conferences[conference_name] = [phone_number,]
        db.destroy()
        return conferences

    def destroy(self):
        """Close our connection to the DB"""
        self.db.destroy()
