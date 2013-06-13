from bridgebeam import application
from bottle import request, abort
from bridgebeam.models.conference import Conference
from twilio import twiml
from twilio.util import RequestValidator
import logging

log = logging.getLogger('bridgebeam')

def validate_twiml():
    twilio_signature = request.get_header('X-Twilio-Signature')
    params = request.forms
    url = application.config.Twiml.callback_base_url + request.fullpath
    auth_token = application.config.Twilio.auth_token
    validator = RequestValidator(auth_token)
    validation = validator.validate(url, params, twilio_signature)
    log.debug("Validator: {}".format(validation))
    log.debug("Twilio-signature: {}\r".format(twilio_signature) + \
              "Params: {}\r".format(params) + \
              "Url: {}".format(url))
    return validation

@application.route('/twiml/join/<conference_uuid>', method='POST')
def join(conference_uuid):
    """
    TwiML Endpoint for for Twilio join callbacks

    Has two modes depending on the value of POST variable 'Digits':
      - != 1: Ask the caller to press 1 to join the bridge
      - == 1: Join the caller to the conference bridge

    """
    if validate_twiml() == False:
        abort(403, 'Validation failed')
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
        log.info("caller is now entering conference_uuid: {}".format(conference_uuid))
        return str(r)
    else:
        log.info("caller will be prompted to join")
        with r.gather(timeout=10, numDigits=1) as g:
            g.say("You have been requested to join the conference bridge named, {}".format(conference_name))
            g.say("To accept, please press one")
        r.redirect('{}/twiml/join/{}'.format(application.config.Twiml.callback_base_url, conference_uuid), method='POST')
        log.debug("sending join prompt now")
        log.debug("sending twiml: {}".format(str(r)))
        return str(r)

@application.route('/twiml/quit', method='POST')
def quit():
    """
    TwiML Endpoint for for Twilio quit callbacks

    Logically removes the call from bridge beam conferences

    """
    if validate_twiml() == False:
        abort(403, 'Validation failed')
    call_sid = request.forms.get('CallSid')
    log.debug("received quit from {}".format(call_sid))
    Conference.remove_from_conferences(call_sid)
