# Twilio SMS Troubleshooting Guide

## Issue: 415 Error on /api/messages/send-bulk

**Symptoms:**
- SMS webhook returns 200 OK (Success)
- Immediately followed by a 415 Error on `/api/messages/send-bulk`
- User receives the SMS reply, but the error appears in logs

**Cause:**
Twilio is configured to send a **Status Callback** or **Fallback** request to `/api/messages/send-bulk`. Since this endpoint expects JSON but Twilio sends form data, it fails with 415.

## 🔧 How to Fix

### 1. Check Phone Number Configuration

1. Go to **Twilio Console** > **Phone Numbers** > **Manage** > **Active Numbers**.
2. Click on your phone number.
3. Scroll down to **Messaging Configuration**.
4. **Verify these settings:**

   - **A MESSAGE COMES IN**:
     - URL: `https://your-domain.com/webhook/sms` (or ngrok URL)
     - Method: `HTTP POST`
   
   - **PRIMARY HANDLER FAILS**: 
     - **MUST BE EMPTY** (Clear this field if it has any URL)
   
   - **STATUS CALLBACK URL**:
     - **MUST BE EMPTY** (Clear this field if it has any URL)

5. Click **Save**.

### 2. Check Messaging Service (If using one)

If you are using a Messaging Service (e.g., for Copilot features):

1. Go to **Messaging** > **Services**.
2. Select your service.
3. Click **Integration** in the left menu.
4. **Verify these settings:**

   - **Incoming Messages**:
     - **Send a webhook**: Selected
     - Request URL: `https://your-domain.com/webhook/sms`
   
   - **Fallback URL**:
     - **MUST BE EMPTY**
   
   - **Callback URL** (or Status Callback):
     - **MUST BE EMPTY**

5. Click **Save**.

### 3. Verify Fix

1. Send an SMS to your Twilio number: `AJUDA`
2. Check your server logs.
3. You should see **ONLY** the `POST /webhook/sms` request.
4. You should **NOT** see any `POST /api/messages/send-bulk` requests.

---

## Why this happens?
When you send a bulk message via API, you might have set a `StatusCallback` parameter, or copied the URL into the console settings by mistake. The webhook endpoint (`/webhook/sms`) handles the reply directly by returning XML (TwiML), so no secondary API call is needed.
