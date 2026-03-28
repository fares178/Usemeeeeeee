# Deployment Guide

## Architecture Overview

This project has **TWO separate parts** that need to be deployed in different places:

### 1. Frontend (HTML/CSS/JavaScript) 
**Location:** GitHub Pages  
**Files:** `index.html`, `settings.html`, `about.html`, `config.js`  
**Status:** ✅ Already working on GitHub Pages

### 2. Backend (Python/Flask)
**Location:** Separate backend service (NOT GitHub Pages)  
**Files:** `chatbot.py`, `requirements.txt`, `templates/`  
**Status:** ❌ Needs to be deployed

---

## How to Deploy the Backend

### Option 1: Deploy to **Render** (Recommended - Free)

1. **Sign up** at https://render.com (free tier available)

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name:** `usemee-chatbot` (or any name)
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python chatbot.py`

3. **Copy the URL** (will be like `https://usemee-chatbot.onrender.com`)

4. **Update config.js** in your GitHub repo:
   ```javascript
   const BACKEND_URL = 'https://usemee-chatbot.onrender.com';
   ```

5. **Commit and push** to GitHub

---

### Option 2: Deploy to **Railway** (Free tier available)

1. **Sign up** at https://railway.app (GitHub login)

2. **Connect your project:**
   - New Project → GitHub Repo
   - Select this repository

3. **Set environment variables** (if needed)

4. **Deploy** - Railway auto-detects the Procfile

5. **Get the URL** from Railway dashboard and update `config.js`

---

### Option 3: Deploy to **Heroku** (May have costs)

1. **Sign up** at https://heroku.com

2. **Create a new app**

3. **Deploy using Git:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **Get the URL** and update `config.js`

---

## Testing Locally

To test the backend locally:

```bash
cd /workspaces/Usemeeeeeee
pip install -r requirements.txt
python chatbot.py
```

Then open your browser:
- Frontend: `http://localhost:8000`
- API: `http://localhost:8000/chat` (POST with `{"message": "hello"}`)

---

## Troubleshooting

### Error: "Connection Error: Backend is not running"
- **Solution:** The backend URL is wrong or the backend isn't deployed
- Check `config.js` has the correct backend URL
- Verify the backend service is running

### Error: "HTTP 500" or "Backend Error"
- **Solution:** There's an error in the Flask app
- Check the backend service logs in Render/Railway dashboard
- Make sure `model_cache/` directory exists with the model files

### Model Loading Error
- **Solution:** Ensure `model_cache/` directory is deployed with the app
- The `sentence-transformers` model should be cached locally

---

## Next Steps

1. **Choose a deployment platform** (Render recommended for free tier)
2. **Deploy the backend** following the instructions above
3. **Get your backend URL** (e.g., `https://usemee-chatbot.onrender.com`)
4. **Update `config.js`** with your backend URL
5. **Commit and push** to GitHub
6. **Test** the chatbot on GitHub Pages

Once deployed, your frontend (on GitHub Pages) will communicate with your backend service! 🎉
