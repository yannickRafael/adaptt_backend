import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except Exception as e:
    logging.error(f"Failed to initialize Twilio client: {e}")
    client = None

def send_single_sms(message, phone_number):
    """
    Sends a single SMS message.
    Returns: (success: bool, message_sid: str or None, error: str or None)
    """
    if not client:
        return False, None, "Twilio client not initialized"
    
    if not TWILIO_PHONE_NUMBER:
        return False, None, "Twilio phone number not configured"
    
    try:
        message_obj = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        logging.info(f"SMS sent to {phone_number}: {message_obj.sid}")
        return True, message_obj.sid, None
    except TwilioRestException as e:
        logging.error(f"Twilio error sending to {phone_number}: {e}")
        return False, None, str(e)
    except Exception as e:
        logging.error(f"Error sending SMS to {phone_number}: {e}")
        return False, None, str(e)

def send_bulk_sms(message, phone_numbers):
    """
    Sends SMS to multiple phone numbers.
    Returns: {
        'total': int,
        'successful': int,
        'failed': int,
        'results': [{'phone': str, 'success': bool, 'message_sid': str, 'error': str}]
    }
    """
    results = []
    successful = 0
    failed = 0
    
    for phone_number in phone_numbers:
        success, message_sid, error = send_single_sms(message, phone_number)
        
        results.append({
            'phone': phone_number,
            'success': success,
            'message_sid': message_sid,
            'error': error
        })
        
        if success:
            successful += 1
        else:
            failed += 1
    
    return {
        'total': len(phone_numbers),
        'successful': successful,
        'failed': failed,
        'results': results
    }

def send_whatsapp_message(message, phone_number):
    """
    Sends a WhatsApp message via Twilio.
    Returns: (success: bool, message_sid: str or None, error: str or None)
    """
    if not client:
        return False, None, "Twilio client not initialized"
    
    if not TWILIO_PHONE_NUMBER:
        return False, None, "Twilio phone number not configured"
    
    try:
        # WhatsApp numbers must be prefixed with 'whatsapp:'
        message_obj = client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
            to=f'whatsapp:{phone_number}'
        )
        logging.info(f"WhatsApp message sent to {phone_number}: {message_obj.sid}")
        return True, message_obj.sid, None
    except TwilioRestException as e:
        logging.error(f"Twilio error sending WhatsApp to {phone_number}: {e}")
        return False, None, str(e)
    except Exception as e:
        logging.error(f"Error sending WhatsApp to {phone_number}: {e}")
        return False, None, str(e)
