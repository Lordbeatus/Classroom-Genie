# Classroom Genie - Deployment Guide

## Deploy to Render (Free Tier)

### Step 1: Deploy Backend (Flask API)

### Step 1: Deploy Backend (Flask API)

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository**:
   - Select `Classroom-Genie` repository
   - Click "Connect"

4. **Configure the service**:
   - **Name**: `classroom-genie-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r Website/website/server/requirements.txt`
   - **Start Command**: `gunicorn --chdir Website/website/server app:app`
   - **Instance Type**: `Free`

5. **Add Environment Variables**:
   - Click "Advanced" → "Add Environment Variable"
   - `HUGGINGFACE_API_KEY`: Your new Hugging Face API token
   - `FLASK_SECRET_KEY`: Generate a random string (e.g., `your-secret-key-here`)

6. **Deploy** - Wait for backend to deploy (5-10 minutes)

7. **Copy the backend URL** (will be something like `https://classroom-genie-api.onrender.com`)

### Step 2: Deploy Frontend (React App)

1. **Click "New +" → "Static Site"**

2. **Connect the same GitHub repository**

3. **Configure the static site**:
   - **Name**: `classroom-genie-frontend`
   - **Branch**: `main`
   - **Build Command**: `cd Website/website/client && npm install && npm run build`
   - **Publish Directory**: `Website/website/client/build`

4. **Add Environment Variable**:
   - `REACT_APP_API_URL`: Use your backend URL from Step 1 (e.g., `https://classroom-genie-api.onrender.com`)

5. **Deploy** - Frontend will build and deploy

### Step 3: Test Your Deployment

Your app will be available at:
- **Frontend**: `https://classroom-genie-frontend.onrender.com`
- **Backend API**: `https://classroom-genie-api.onrender.com`

### ⚠️ Important Notes for Free Tier:

1. **Generate NEW Hugging Face API Key**: 
   - Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
   - Delete the old exposed token
   - Create a new one for deployment

2. **Free Tier Limitations**:
   - Services sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds to wake up
   - 750 hours/month limit (enough for personal projects)

3. **Deploy Backend FIRST**, then Frontend (so you have the API URL)

### Troubleshooting:

- **Build fails**: Check the logs in Render dashboard
- **CORS errors**: Make sure your backend URL is correct in frontend env vars
- **API not responding**: Wait for backend to fully deploy before testing frontend

## Local Development:
```bash
# Backend
cd Website/website/server
pip install -r requirements.txt
python app.py

# Frontend  
cd Website/website/client
npm install
npm start
```
