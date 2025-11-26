# Twilio Bulk Messaging - Configuration Guide

## Environment Variables

Add the following to your `.env` file:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+258XXXXXXXXX  # Your Twilio phone number
```

## Getting Twilio Credentials

1. Sign up at https://www.twilio.com/
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase a phone number or use the trial number

## API Usage

### Send Bulk SMS

**Endpoint:** `POST /api/messages/send-bulk`

**Request:**
```json
{
  "message": "Olá! Esta é uma mensagem de teste.",
  "phone_numbers": [
    "+258841234567",
    "+258849876543"
  ]
}
```

**Response:**
```json
{
  "total": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "phone": "+258841234567",
      "success": true,
      "message_sid": "SM...",
      "error": null
    },
    {
      "phone": "+258849876543",
      "success": true,
      "message_sid": "SM...",
      "error": null
    }
  ]
}
```

## Features

- ✅ Bulk SMS sending
- ✅ Individual error tracking per phone number
- ✅ WhatsApp messaging support (via `send_whatsapp_message`)
- ✅ Comprehensive logging
- ✅ Error handling for Twilio API failures
