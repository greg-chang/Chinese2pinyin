from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from flask import Flask, request
import os

load_dotenv()

# Twilio Account SID and Auth Token
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

# Your Twilio phone number
twilio_phone_number = '+18446041707'

# Your phone number and your mom's phone number
your_phone_number = '+19496776541'
mom_phone_number = '+19499817768'

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_notification(message):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=your_phone_number
    )

def process_incoming_sms(request):
    from_number = request.values.get('From', None)
    body = request.values.get('Body', '').strip()

    if from_number == mom_phone_number:
        send_notification(f"You have a text from your mom: {body}")

if __name__ == "__main__":
    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/sms", methods=['POST'])
    def receive_sms():
        response = MessagingResponse()
        process_incoming_sms(request)
        return str(response)

    app.run(debug=True)
