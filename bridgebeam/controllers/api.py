from bridgebeam import application
from bottle import request
from bridgebeam.models.conference import Conference
import json
import logging

log = logging.getLogger('bridgebeam')

@application.route('/api/v1/conference/list', method='GET')
def list_conferences():
    """Return a json object of all conferences and their connected numbers"""
    conferences = Conference.get_conferences()
    for conference in conferences.keys():
        private_numbers = []
        for number in conferences[conference]:
            private_numbers.append((number[:-7] + 'xxx' + number[-4:]))
        conferences[conference] = private_numbers
    return json.dumps(conferences)

@application.route('/api/v1/conference/join', method='POST')
def join_conference():
    """
    The endpoint for clients to join phone numbers to conferences

    POST Vars:
      - conference_name: Case-sensitive alphanumeric with whitespace
      - phone_number: Numerals with any formatting

    """
    conference_name = str(request.forms.get('conference_name'))
    conference = Conference(name=conference_name)
    # uuid is generated if the conference_name is okay
    if conference.uuid:
        phone_number = str(request.forms.get('phone_number'))
        if phone_number:
            # calling the user now
            log.info('JOIN - {} connected to {}'.format(phone_number,
                                                        conference_name)) 
            conference.call_out(phone_number)
            conference.destroy()
            return "success"
