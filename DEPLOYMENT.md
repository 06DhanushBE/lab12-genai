# 🚀 Easy Deployment Guide

## **Option 1: Railway (Recommended - Easiest)**

### Why Railway?

- ✅ **Zero configuration** - Just connect GitHub
- ✅ **Free tier** with generous limits
- ✅ **Auto-detects** Streamlit apps
- ✅ **Simple** environment variables
- ✅ **Fast** deployment (2-3 minutes)

### Steps:

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select `06DhanushBE/lab12-genai`**
5. **Add Environment Variables:**
   - Go to Variables tab
   - Add: `GOOGLE_API_KEY = AIzaSyBu8RmxMPG1kridRDNdLKJMXTnZf5xRBvg`
   - Add: `EXCHANGE_RATE_API_KEY = 89fc1913420cd473fa63bdc2`
6. **Deploy!** - Your app will be live in minutes

---

## **Option 2: Render (Also Great)**

### Steps:

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect `06DhanushBE/lab12-genai`**
5. **Configure:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. **Add Environment Variables:**
   - `GOOGLE_API_KEY = AIzaSyBu8RmxMPG1kridRDNdLKJMXTnZf5xRBvg`
   - `EXCHANGE_RATE_API_KEY = 89fc1913420cd473fa63bdc2`
7. **Deploy!**

---

## **Option 3: Heroku (Classic)**

### Steps:

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: `git push heroku main`
5. **Set environment variables**:
   ```bash
   heroku config:set GOOGLE_API_KEY="AIzaSyBu8RmxMPG1kridRDNdLKJMXTnZf5xRBvg"
   heroku config:set EXCHANGE_RATE_API_KEY="89fc1913420cd473fa63bdc2"
   ```

---

## **🎯 My Recommendation: Use Railway**

Railway is the easiest option for Streamlit apps. It requires zero configuration and works perfectly with your current setup.

**Just go to [railway.app](https://railway.app) and follow the steps above!**
