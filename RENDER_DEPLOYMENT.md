# 🚀 Render Deployment Guide

## Step 1: Create GitHub Repository

1. **Go to GitHub** (https://github.com)
2. **Create new repository:**
   - Name: `james-whatsapp-capi`
   - Visibility: Private (recommended) or Public
   - **Don't** initialize with README
3. **Copy the repository URL**

## Step 2: Push Code to GitHub

Open terminal and run:

```bash
cd "/home/pc/Documents/Nitu's folder/james"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "WhatsApp to Meta CAPI integration"

# Add remote (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/james-whatsapp-capi.git

# Push
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

1. **Go to Render:** https://render.com/
2. **Sign Up/Login:**
   - Use GitHub account (easiest)
   - Authorize Render to access your repositories

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your `james-whatsapp-capi` repository
   - Render auto-detects the `render.yaml` file

4. **Configure (if not auto-detected):**
   - **Name:** james-whatsapp-capi
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

5. **Add Environment Variables:**
   - Click "Environment" tab
   - Add variables:
     ```
     META_PIXEL_ID = 1200365651983145
     META_ACCESS_TOKEN = EAARmZBfr0FDABQVTh3zq9sRFJ5BLxHA2gfsZA0xyudB0fZBZBfrp23MKBKlXfZB0QpHFLYSA9mKqJ7yfxZBcDJOQquLbZCWmPnKk2LfCHkfknscCJpfF7LvVZBZC9MSmm93qTMKoKfQDuA8cYxPHVbVXwnKFaOZAcbyVYiZA2F3M8p7U06IAPdn8qUlKoBmUHU6ZAS0y3gZDZD
     ```

6. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-5 minutes for build
   - Render will show: "Your service is live at https://james-whatsapp-capi.onrender.com"

## Step 4: Verify Deployment

Test the health endpoint:

```bash
curl https://james-whatsapp-capi.onrender.com/health
```

Expected response:
```json
{"status":"healthy","meta_pixel_id":"1200365651983145","api_version":"v18.0"}
```

## Step 5: Update ManyChat

1. Go to ManyChat flow
2. Click on "External Request" action
3. Update URL to:
   ```
   https://james-whatsapp-capi.onrender.com/webhook
   ```
4. Save and Set Live

## Step 6: Test End-to-End

1. Send WhatsApp message to: +447926680847
2. Check Render logs (Dashboard → Logs)
3. Should see:
   ```
   ✅ Event sent successfully!
   Events received: 1
   FBTrace ID: xyz123
   ```
4. Check Events Manager for event

## ✅ Done!

Your webhook is now live 24/7!

**Webhook URL:** `https://james-whatsapp-capi.onrender.com/webhook`

---

## 🔧 Troubleshooting

### Logs Not Showing Events?
- Check Render dashboard → Logs tab
- Verify environment variables are set
- Test health endpoint

### ManyChat Not Triggering?
- Verify webhook URL in ManyChat (must end with `/webhook`)
- Check ManyChat flow is "Live"
- Verify ad triggers are enabled

### Deployment Failed?
- Check requirements.txt exists
- Verify Python version in runtime.txt
- Check Render build logs for errors

---

## 📊 Monitoring

**Render Dashboard:**
- View logs in real-time
- Monitor uptime
- Check resource usage

**Free Tier Limits:**
- Service sleeps after 15 min of inactivity
- Wakes up on first request (may take 30-60 seconds)
- 750 hours/month free

**For production:** Upgrade to paid plan ($7/month) for:
- No sleeping
- Better performance
- Priority support
