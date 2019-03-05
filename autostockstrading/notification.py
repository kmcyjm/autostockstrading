
from autostockstrading import twilioAccountId, twilioAuthToken, twilioFromPhoneNumber, twilioToPhoneNumber
from twilio.rest import Client

class SendNotification:
    def __init__(self):
        pass

    def send_sms(self, message):
        # Your Account SID from twilio.com/console
        account_sid = twilioAccountId
        # Your Auth Token from twilio.com/console
        auth_token = twilioAuthToken

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to=twilioToPhoneNumber,
            from_=twilioFromPhoneNumber,
            body=message)

        print(message.sid)
