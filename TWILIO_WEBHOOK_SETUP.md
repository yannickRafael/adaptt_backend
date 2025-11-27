# Twilio Webhook Configuration Guide

## Prerequisites
- Twilio account with active phone number
- Flask app running (locally or deployed)
- ngrok (for local development) or public domain

---

## Step 1: Expose Your Local Server (Development)

### Install ngrok
```bash
# Download from https://ngrok.com/download
# Or install via package manager
```

### Start ngrok
```bash
ngrok http 5001
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5001
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

---

## Step 2: Configure SMS Webhook

### 1. Go to Twilio Console
https://console.twilio.com/

### 2. Navigate to Phone Numbers
- Click **Phone Numbers** → **Manage** → **Active Numbers**
- Click on your phone number

### 3. Configure Messaging
Scroll to **Messaging Configuration**

**A MESSAGE COMES IN:**
- Select: **Webhook**
- URL: `https://abc123.ngrok.io/webhook/sms`
- Method: **HTTP POST**

### 4. Save
Click **Save** at the bottom

---

## Step 3: Configure WhatsApp Webhook

### Option A: WhatsApp Sandbox (Testing)

#### 1. Go to WhatsApp Sandbox
https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

#### 2. Join Sandbox
- Send the join code from your WhatsApp to the sandbox number
- Example: Send `join abc-xyz` to `+1 415 523 8886`

#### 3. Configure Webhook
**WHEN A MESSAGE COMES IN:**
- URL: `https://abc123.ngrok.io/webhook/whatsapp`
- Method: **HTTP POST**

#### 4. Save Configuration

### Option B: WhatsApp Business API (Production)

#### 1. Go to Messaging Services
https://console.twilio.com/us1/develop/sms/services

#### 2. Create/Select Service
- Click your messaging service
- Go to **Senders** → Add your WhatsApp sender

#### 3. Configure Inbound Settings
**PROCESS INBOUND MESSAGES:**
- URL: `https://your-domain.com/webhook/whatsapp`
- Method: **HTTP POST**

---

## Step 4: Test the Configuration

### Test SMS
Send an SMS to your Twilio number:
```
AJUDA
```

You should receive a response with available commands.

### Test WhatsApp
Send a WhatsApp message to your sandbox/business number:
```
AJUDA
```

You should receive the same response.

---

## Step 5: Verify Webhooks are Working

### Check Logs
In your Flask terminal, you should see:
```
INFO - SMS received from +258844236139: AJUDA
```

### Check Twilio Debugger
https://console.twilio.com/us1/monitor/logs/debugger

Look for recent webhook calls and verify they're successful (status 200).

---

## Production Deployment

### 1. Deploy Your Flask App
Deploy to:
- Heroku
- AWS EC2
- Google Cloud Run
- DigitalOcean
- etc.

### 2. Get Public URL
Example: `https://adaptt-api.herokuapp.com`

### 3. Update Twilio Webhooks
Replace ngrok URL with your production URL:
- SMS: `https://adaptt-api.herokuapp.com/webhook/sms`
- WhatsApp: `https://adaptt-api.herokuapp.com/webhook/whatsapp`

---

## Troubleshooting

### Webhook Returns Error
**Check:**
- Flask app is running
- ngrok is active (for local dev)
- Webhook URL is correct
- URL uses HTTPS (required by Twilio)

### No Response Received
**Check:**
- Twilio debugger for error messages
- Flask logs for incoming requests
- Phone number is correct
- Message format is correct

### "Command not recognized"
**Check:**
- Command spelling (case-insensitive)
- Command format matches examples
- No extra spaces

---

## Quick Reference

### Webhook URLs
```
SMS:      https://YOUR-DOMAIN/webhook/sms
WhatsApp: https://YOUR-DOMAIN/webhook/whatsapp
```

### Test Commands
```
AJUDA
REGISTRAR Test User maputo
LISTAR
SUBSCREVER [project-id]
CANCELAR [project-id]
```

### Twilio Console Links
- **Phone Numbers**: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming
- **WhatsApp Sandbox**: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
- **Debugger**: https://console.twilio.com/us1/monitor/logs/debugger

---

## Security Notes

### Production Checklist
- [ ] Use HTTPS only
- [ ] Validate Twilio signature (optional but recommended)
- [ ] Rate limit webhook endpoints
- [ ] Monitor for abuse
- [ ] Keep Twilio credentials secure

### Validate Twilio Requests (Optional)
Add to your webhook endpoints:
```python
from twilio.request_validator import RequestValidator

validator = RequestValidator(TWILIO_AUTH_TOKEN)
signature = request.headers.get('X-Twilio-Signature', '')
url = request.url
params = request.form

if not validator.validate(url, params, signature):
    return 'Invalid request', 403
```

---

## Need Help?

- **Twilio Docs**: https://www.twilio.com/docs/sms/twiml
- **Twilio Support**: https://support.twilio.com/
- **Check Logs**: Your Flask terminal and Twilio debugger
