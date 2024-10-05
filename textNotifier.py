from twilio.rest import Client
from dotenv import load_dotenv
from pypinyin import pinyin
import re 
import os
import time

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

# Your mom's phone number and your phone number
twilio_phone_number =   '+18446041707'
mom_phone_number =      '+19499817768'
flo_phone_number =      '+19499813381'
your_phone_number =     '+19496776541'

chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Initialize a variable to keep track of the latest message timestamp & response sent flag
latest_message_timestamp = None
response_sent = False

def chinese2pinyin(phrase):
    chinese_text = phrase.group()
    pinyin_text = ' '.join([' '.join(p) for p in pinyin(chinese_text)])
    return pinyin_text
    
print(f'mom_phone_number: {mom_phone_number}')
print(f'your_phone_number: {your_phone_number}')

while True:
    # Retrieve the latest message from mom
    try:
        messages = client.messages.list(to=twilio_phone_number)
    except Exception as e:
        print(f"Error when checking for messages: {e}")

    latest_message = None   
    print('Checking for new messages...')

    for message in messages:
        if message.from_ == flo_phone_number:
            if latest_message is None or message.date_created > latest_message.date_created:
                latest_message = message


    # Process the latest message, if it exists
    if latest_message and latest_message.date_created != latest_message_timestamp:
        print(f"--og_msg--> {latest_message.body}")
        translated_message = chinese_pattern.sub(chinese2pinyin, latest_message.body)
        print(f"--pinyin--> {translated_message}")
        
        latest_message_timestamp = latest_message.date_created
        
        if not response_sent:
            message = client.messages.create (
                to=your_phone_number,
                from_=twilio_phone_number,  # Use your Twilio phone number or another valid Twilio number
                body=f"Original message:\n{latest_message.body} \nTranslated message:\n{translated_message}"
            )
            # Update latest message timestamp
            print('Response sent.')
            response_sent = True
            
    # Reset the response sent flag when there's no new message
    elif not latest_message:
        response_sent = False
    
    # checks for new messages every 10sec
    time.sleep(5)
    
    