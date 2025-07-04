# Classroom Genie - Deployment Guide

## Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** (already done!)

2. **Go to [Render Dashboard](https://dashboard.render.com/)**

3. **Create New → Blueprint**
   - Connect your GitHub repo: `Classroom-Genie`
   - Render will automatically detect the `render.yaml` file

4. **Set Environment Variables**:
   - `HUGGINGFACE_API_KEY`: Your new Hugging Face API token
   - `FLASK_SECRET_KEY`: Will be auto-generated

5. **Deploy!** Render will create both frontend and backend services.

### Option 2: Manual Setup

#### Backend (Flask API):
1. Create New → Web Service
2. Connect GitHub repo
3. Settings:
   - **Build Command**: `pip install -r Website/website/server/requirements.txt`
   - **Start Command**: `gunicorn --chdir Website/website/server app:app`
   - **Environment**: Python 3

#### Frontend (React):
1. Create New → Static Site
2. Connect GitHub repo  
3. Settings:
   - **Build Command**: `cd Website/website/client && npm install && npm run build`
   - **Publish Directory**: `Website/website/client/build`

### Environment Variables Needed:
- `HUGGINGFACE_API_KEY`: Your Hugging Face API token
- `REACT_APP_API_URL`: URL of your deployed backend (e.g., `https://your-api-name.onrender.com`)

### Important Notes:
- Backend will be available at: `https://classroom-genie-api.onrender.com`
- Frontend will be available at: `https://classroom-genie-frontend.onrender.com`
- Make sure to generate a NEW Hugging Face API key since the old one was exposed!

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
