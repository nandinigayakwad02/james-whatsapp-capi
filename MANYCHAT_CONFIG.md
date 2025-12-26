# ManyChat Webhook Configuration Guide

## ✅ Your Backend is LIVE!

**Public URL:** `https://six-taxis-glow.loca.lt`

**Webhook Endpoint:** `https://six-taxis-glow.loca.lt/webhook`

---

## 📱 Configure ManyChat (Step-by-Step)

### Step 1: Open ManyChat Flow Builder

1. Go to ManyChat dashboard
2. Navigate to **Automation** → **Flows**
3. Open your WhatsApp appointment flow (or create new)

### Step 2: Add Webhook Action

1. In your flow, add an **Action** block
2. Select **"External Request"**
3. Place it at the point where conversation starts

### Step 3: Configure External Request

**Settings:**
- **Request Type:** `POST`
- **URL:** `https://six-taxis-glow.loca.lt/webhook`
- **Headers:** (leave default)

**Body (JSON):**
```json
{
  "phone": "{{phone}}",
  "timestamp": "{{timestamp}}",
  "flow_name": "WhatsApp Appointment Flow",
  "user_id": "{{subscriber_id}}",
  "full_name": "{{full_name}}"
}
```

### Step 4: Map ManyChat Variables

Make sure these ManyChat variables are available:
- `{{phone}}` - User's phone number
- `{{subscriber_id}}` - ManyChat subscriber ID
- `{{full_name}}` - User's name (if collected)
- `{{timestamp}}` - Current timestamp

If not available, use Custom Fields or System Fields.

### Step 5: Save & Test

1. Click **Save** on the action block
2. Activate the flow
3. Send a test WhatsApp message

---

## 🧪 Testing

### Test from WhatsApp:
1. Send message to your ManyChat WhatsApp number
2. Trigger the flow with webhook

### Check Backend Logs:
Look for:
```
📨 Webhook received from ManyChat
   Phone: ********1234
   Flow: WhatsApp Appointment Flow
🚀 Sending event to Meta CAPI
✅ Event sent successfully!
```

### Verify in Meta Events Manager:
1. Go to Events Manager: https://business.facebook.com/events_manager
2. Select Pixel: `1554292762526086`
3. Click **Test Events** tab
4. Look for `whatsapp_conversation_started` event
5. (Events appear within 5-20 minutes)

---

## ⚠️ Important Notes

### Localtunnel Security:
- First time accessing the URL, you'll see a warning page
- Click **"Continue"** to proceed
- This is normal for localtunnel

### URL Will Change:
- This tunnel URL expires when you close terminal
- Each restart gives new URL
- For production, use ngrok or deploy to server

### Keep Terminal Running:
- Don't close the terminal with `lt --port 8000`
- Don't close terminal with `python3 app.py`
- Both must keep running

---

## 🎯 Next Steps After Testing

Once testing is successful:

1. **Get Client's Access Token:**
   - Replace test token in `.env`
   - Use James Corneille's Pixel ID: `597975348758669`

2. **Production Deployment:**
   - Deploy to Heroku/Railway/DigitalOcean
   - Get permanent HTTPS URL
   - Update ManyChat webhook to production URL

3. **Monitor Events:**
   - Check Meta Events Manager regularly
   - Events should appear for every conversation
   - Facebook Ads will optimize based on these events

---

## 📞 Troubleshooting

### Webhook not triggering?
- Check ManyChat flow is active
- Verify URL is correct: `https://six-taxis-glow.loca.lt/webhook`
- Check both terminals are running

### Events not in Meta?
- Events take 5-20 minutes to appear
- Check **Test Events** tab, not Overview
- Verify access token is valid

### 502 Bad Gateway?
- Server might have stopped
- Restart `python3 app.py`
- Restart `lt --port 8000`

---

**Ready to configure ManyChat! 🚀**
