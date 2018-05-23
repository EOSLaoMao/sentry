from twilio.rest import Client
from config import (TWILIO_ACCOUNT_SID,
                    TWILIO_AUTH_TOKEN,
                    PHONE_FROM,
                    PHONES)

def call():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for phone in PHONES:
        call = client.calls.create(
                                url='http://demo.twilio.com/docs/voice.xml',
                                to=phone,
                                from_=PHONE_FROM
                            )

        print(call.sid)

if __name__ == '__main__':
    call()
