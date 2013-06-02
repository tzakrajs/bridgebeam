from bridgebeam import application
from bottle import request
from bridgebeam.models.conference import Conference, remove_from_conferences
from twilio import twiml
import logging

log = logging.getLogger('bridgebeam')

@application.route('/twiml/join/<conference_uuid>', method='POST')
def join(conference_uuid):
    log.debug("received join on {}".format(conference_uuid))
    conference = Conference(uuid=conference_uuid)
    conference_name = conference.get_name()
    log.debug("using conference_uuid {}, determined conference_name is: {}".format(conference_uuid, conference_name))
    call_sid = request.forms.get('CallSid')
    log.debug("caller has call_sid: {}".format(call_sid))
    phone_number = request.forms.get('To')
    log.debug("caller has phone_number: {}".format(phone_number))
    r = twiml.Response() 
    digits = request.forms.get('Digits')
    if digits:
        log.debug("caller has entered digits: {}".format(digits))
    if digits == '1':
        log.debug("caller has pressed one to join")
        conference.add(call_sid, phone_number)
        r.say("Now joining you to the conference bridge named, {}".format(conference_name))
        d = twiml.Dial()
        d.append(twiml.Conference(conference_uuid))
        r.append(d)
        log.debug("caller is now entering conference_uuid: {}".format(conference_uuid))
        return str(r)
    else:
        log.debug("caller will be prompted to join")
        with r.gather(timeout=10, numDigits=1) as g:
            g.say("You have been requested to join the conference bridge named, {}".format(conference_name))
            g.say("To accept, please press one")
        r.redirect('http://somedomain.com/twiml/join/{}'.format(conference_uuid), method='POST')
        log.debug("sending join prompt now")
        log.debug("sending twiml: {}".format(str(r)))
        return str(r)

@application.route('/twiml/quit', method='POST')
def quit():
    call_sid = request.forms.get('CallSid')
    log.debug("received quit from {}".format(call_sid))
    remove_from_conferences(call_sid)
