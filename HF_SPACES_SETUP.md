# Hugging Face Spaces Integration Guide

## Setup Instructions

### Step 1: Get Your Hugging Face Space URL

1. Go to https://huggingface.co/spaces
2. Find your chatbot space
3. Copy the URL (should look like: `https://your-username-chatbot.hf.space`)

### Step 2: Update config.js

Open `config.js` and replace:
```javascript
const BACKEND_URL = localStorage.getItem('backendUrl') || 'https://YOUR-USERNAME-chatbot.hf.space';
```

With your actual Space URL:
```javascript
const BACKEND_URL = localStorage.getItem('backendUrl') || 'https://faresfady2010-business-chatbot.hf.space';
```

### Step 3: Commit and Push

```bash
git add config.js
git commit -m "Update HF Space URL"
git push origin main
```

---

## Common Issues & Solutions

### Issue 1: "Cannot reach Hugging Face Space"

**Possible causes:**

1. **Space is in "sleep" mode**
   - Free tier HF Spaces go to sleep after inactivity
   - **Solution:** Visit your Space URL directly to wake it up, then try the chatbot
   - Or upgrade to a paid plan to keep it always running

2. **Wrong URL in config.js**
   - **Check:** Does `BACKEND_URL` match your actual Space URL?
   - **Solution:** Copy the exact URL from your Space

3. **Space not accessible from browser**
   - **Check:** Can you visit `https://your-space-url.hf.space` directly in your browser?
   - If not, your Space might have a permission issue

### Issue 2: "Got a different response format than expected"

HF Spaces can return data in different formats depending on how it's configured.

**Check your Space's Gradio interface:**
- Does it have an API tab?
- What is the expected input/output format?

Common formats:
- `{"response": "answer"}` - Flask format
- `{"data": ["answer"]}` - HF Spaces Gradio format
- `{"result": "answer"}` - Alternative format

Our code now tries multiple formats, but if your Space returns something different, let me know!

### Issue 3: "CORS Error" in browser console

**This usually means:**
- Browser is blocking the request from GitHub Pages to your HF Space
- Not all HF Spaces have CORS enabled

**Workaround:**
If you see CORS errors, you'll need to:
1. Deploy the Flask backend to a backend service (Render, Railway, Heroku)
2. Or configure your HF Space to enable CORS

---

## Testing Your Integration

### From Browser Console

Open your browser's **Developer Tools** (F12) and go to **Console**, then run:

```javascript
// Check if config is loaded
console.log('Backend URL:', BACKEND_URL);
console.log('Using local:', USE_LOCAL_BACKEND);

// Test the API endpoint
fetch(ACTIVE_BACKEND + "/call/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ data: ["hello"] })
})
.then(r => r.json())
.then(d => console.log('Response:', d))
.catch(e => console.error('Error:', e));
```

### Direct API Test

Replace `YOUR-SPACE-URL` with your actual URL:

```bash
curl -X POST "https://YOUR-SPACE-URL.hf.space/call/predict" \
  -H "Content-Type: application/json" \
  -d '{"data": ["hello"]}'
```

---

## If HF Spaces Doesn't Work...

Try deploying to **Render** instead (free):

1. Go to https://render.com
2. Create a new Web Service
3. Connect your GitHub repo
4. Set these commands:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `python chatbot.py`
5. Get your URL: `https://your-app-name.onrender.com`
6. Update `config.js`:
   ```javascript
   const BACKEND_URL = 'https://your-app-name.onrender.com';
   ```

---

## Debug Mode

To enable more detailed logging, open browser console and run:

```javascript
// Show what URL we're calling
console.log('Calling:', ACTIVE_BACKEND + (USE_LOCAL_BACKEND ? "/chat" : "/call/predict"));
```

Then send a message and look at the console for error details.

---

## Need Help?

1. Check browser console for error messages (F12 → Console)
2. Check if your HF Space is actually running
3. Verify the URL in config.js is exactly correct
4. Try accessing the Space URL directly in your browser first
