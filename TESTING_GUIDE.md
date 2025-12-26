# End-to-End Testing Guide - Production

## ✅ System Status

**Backend:** Running on port 8000
**Pixel ID:** 1200365651983145 (James Corneille Event Data)
**Tunnel URL:** https://whole-glasses-juggle.loca.lt
**Webhook URL:** https://whole-glasses-juggle.loca.lt/webhook

---

## 📋 Step-by-Step Testing

### Step 1: Configure ManyChat Webhook

1. Go to ManyChat → Automations → Flows
2. Open "WA to Facebook Meta" flow
3. Click "Edit" button
4. Click on "External Request" yellow action block
5. Update URL to: `https://whole-glasses-juggle.loca.lt/webhook`
6. Verify Body (JSON):
   ```json
   {
     "phone": "{{phone}}",
     "flow_name": "WhatsApp Test Flow"
   }
   ```
7. Click "Save"
8. Click "Set Live"

---

### Step 2: Send WhatsApp Test Message

1. Open WhatsApp on your phone
2. Send message to: `+447926680847` (James's WhatsApp Business number)
3. Type: "Hello" or "Test"
4. Send the message

---

### Step 3: Watch Backend Logs

You should immediately see (within 2-3 seconds):

```
============================================================
📨 WEBHOOK RECEIVED FROM MANYCHAT
============================================================

🔍 COMPLETE PAYLOAD:
   Phone: +447926680847
   Timestamp: None
   Flow Name: WhatsApp Test Flow
   User ID: None
   Full Name: None
------------------------------------------------------------

📱 Phone (masked): ********0847
🔄 Flow: WhatsApp Test Flow

🚀 Sending event to Meta CAPI: https://graph.facebook.com/v18.0/1200365651983145/events
✅ Event sent successfully!
   Events received: 1
   FBTrace ID: AyEKLyeXI3tLiI8flNwczi1

📤 META API RESPONSE:
   Success: True
   Events Received: 1
   FBTrace ID: AyEKLyeXI3tLiI8flNwczi1
============================================================
```

**✅ = Working!**
**❌ = Check troubleshooting below**

---

### Step 4: Verify in Meta Events Manager

1. Go to: https://business.facebook.com/events_manager
2. Select Pixel: **"James Corneille Event Data"** (ID: 1200365651983145)
3. Click on **"Test Events"** tab (NOT Overview!)
4. Wait 5-20 minutes
5. Look for event:
   - Event Name: `whatsapp_conversation_started`
   - Event Source: `chat`
   - Event Time: [your test time]

---

## 🐛 Troubleshooting

### No logs appear in terminal

**Problem:** ManyChat didn't trigger webhook

**Check:**
- Flow is "Live" (green badge)
- External Request URL is correct
- Message actually triggered the flow
- Localtunnel still running

**Fix:** Retry sending WhatsApp message

---

### Error in backend logs

**Common Errors:**

**❌ "Invalid access token"**
- Token might be expired
- Check `.env` file has correct token

**❌ "Connection refused"**
- Server stopped
- Restart: `python3 app.py`

**❌ "404 Not Found"**
- Webhook URL wrong
- Should end with `/webhook`

---

### Events not in Meta Events Manager

**Reasons:**
1. **Wait time** - Events take 5-20 minutes to appear
2. **Wrong tab** - Must be in "Test Events", not "Overview"
3. **Wrong pixel** - Make sure "James Corneille Event Data" selected
4. **Event failed** - Check backend logs for errors

---

## ✅ Success Checklist

- [ ] ManyChat webhook configured with correct URL
- [ ] Flow is Live
- [ ] WhatsApp message sent
- [ ] Backend logs show "✅ Event sent successfully!"
- [ ] FBTrace ID received
- [ ] Waited 20 minutes
- [ ] Event visible in Meta Events Manager

---

## 🎯 What Success Looks Like

**Backend Terminal:**
```
✅ Event sent successfully!
Events received: 1
FBTrace ID: xyz123
```

**Meta Events Manager:**
- New row in events table
- Event: `whatsapp_conversation_started`
- Green status
- Phone number (hashed)

---

**Ready to test! Follow steps 1-4 above.** 🚀
