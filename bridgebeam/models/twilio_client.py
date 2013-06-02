from bridgebeam import application
from twilio.rest import TwilioRestClient

# load twilio config details
account_sid = application.config.Twilio.account_sid
auth_token = application.config.Twilio.auth_token

# create twilio rest client instance
twilio = TwilioRestClient(account_sid, auth_token)
