# Complete Deployment Guide for Render

This guide walks you through deploying your RAG application to Render's free tier step-by-step.

## Prerequisites Checklist

- [ ] GitHub account created
- [ ] Render account created (https://render.com)
- [ ] Git installed on your computer
- [ ] Your data files ready in JSON format
- [ ] Node.js and npm installed

## Step-by-Step Deployment

### Phase 1: Prepare Your Application

#### 1.1 Add Your Data Files

```bash
# Navigate to the data folder
cd rag-app/data

# Remove sample.json (optional)
rm sample.json

# Add your JSON files here
# Example: copy your files
cp /path/to/your/data/*.json .

# Verify files are there
ls -la
```

Your JSON files should follow this structure:
```json
[
  {
    "id": "unique_id_1",
    "title": "Your Title",
    "description": "Your content here",
    "category": "Category Name"
  }
]
```

#### 1.2 Build the Frontend

```bash
# Go to project root
cd ..

# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Build the production bundle
npm run build

# Verify dist folder was created
ls -la dist/

# You should see:
# - index.html
# - assets/ (folder with JS and CSS files)
```

#### 1.3 Test Locally (Optional but Recommended)

```bash
# Go back to project root
cd ..

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to http://localhost:8000
# Test the chat interface
# Verify your data loads correctly
```

### Phase 2: Push to GitHub

#### 2.1 Initialize Git Repository

```bash
# If not already a git repo
git init

# Check what files will be committed
git status
```

#### 2.2 Verify Important Files Are Included

Make sure these are present:
- [ ] `frontend/dist/` folder (with built files)
- [ ] `data/*.json` files (your actual data)
- [ ] `requirements.txt`
- [ ] `Procfile`
- [ ] `app.py` and all Python files

#### 2.3 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "rag-application")
3. Don't initialize with README (we already have files)
4. Click "Create repository"

#### 2.4 Push Code to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: RAG application with data"

# Add GitHub remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/rag-application.git

# Push to GitHub
git push -u origin main

# If you get an error about 'master' branch, use:
# git branch -M main
# git push -u origin main
```

#### 2.5 Verify on GitHub

1. Go to your repository URL
2. Check that you see:
   - All Python files
   - `frontend/dist/` folder with files
   - `data/` folder with your JSON files
   - `requirements.txt`, `Procfile`, etc.

### Phase 3: Deploy on Render

#### 3.1 Sign Up / Log In to Render

1. Go to https://render.com
2. Sign up with GitHub (recommended) or email
3. Verify your email if required

#### 3.2 Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect GitHub"** if first time
4. Find and select your repository
5. Click **"Connect"**

#### 3.3 Configure Web Service

Fill in these settings:

**Basic Settings:**
- **Name**: `rag-app` (or your choice - this will be in your URL)
- **Region**: Choose closest to your users (Oregon, Frankfurt, Singapore)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**: 
  ```
  uvicorn app:app --host 0.0.0.0 --port 10000
  ```

**Instance Type:**
- Select: **Free** ($0/month)

**Advanced Settings** (click to expand):
- **Auto-Deploy**: `Yes` (recommended)
- **Environment Variables**: Add these:
  - Key: `PYTHON_VERSION`, Value: `3.11.0`

#### 3.4 Create Web Service

1. Review all settings
2. Click **"Create Web Service"**
3. Deployment will start automatically

### Phase 4: Monitor Deployment

#### 4.1 Watch the Logs

You'll see the deployment process in real-time:

```
==> Downloading Python 3.11.0
==> Installing dependencies
==> Collecting fastapi
==> Collecting sentence-transformers
==> Installing sentence-transformers (this is large, ~500MB)
==> Starting server
==> ========================================
==> Starting RAG Application
==> ========================================
==> 1. Initializing database...
==>    Database has 0 records
==> 2. Loading data from JSON files...
==>    Loaded sample.json: 2 records
==> 3. Initializing embedding model...
==>    Loading embedding model: all-MiniLM-L6-v2
==> 4. Building FAISS index...
==>    Generating embeddings for 2 texts...
==>    Building FAISS index with 2 vectors...
==> 5. Initializing RAG search...
==> ========================================
==> RAG Application Ready!
==> Total records: 2
==> ========================================
```

#### 4.2 Deployment Timeline

- **Building**: 2-3 minutes
- **Installing Python packages**: 3-5 minutes
- **Downloading embedding model**: 1-2 minutes
- **Loading data & building index**: 1-2 minutes
- **Total**: ~10-15 minutes for first deployment

#### 4.3 Check for Success

Look for these indicators:
- ✅ Green status indicator
- ✅ "Live" badge on your service
- ✅ URL is clickable (e.g., `https://rag-app.onrender.com`)

### Phase 5: Test Your Deployed Application

#### 5.1 Access Your Application

1. Click the URL (e.g., `https://rag-app.onrender.com`)
2. Wait 30-60 seconds for cold start (first time only)
3. You should see the chat interface

#### 5.2 Test the Chat

1. Type a question related to your data
2. Click "Send"
3. You should get a response based on your knowledge base

#### 5.3 Check Health Endpoint

Visit: `https://rag-app.onrender.com/health`

Should show:
```json
{
  "status": "healthy",
  "records": 150,
  "index_ready": true
}
```

## Troubleshooting Common Issues

### Issue: "Application failed to start"

**Check:**
1. Look at deployment logs for Python errors
2. Verify `requirements.txt` has all dependencies
3. Make sure `frontend/dist/` folder exists and was pushed

**Fix:**
```bash
# Rebuild frontend
cd frontend
npm run build
cd ..

# Commit and push
git add frontend/dist
git commit -m "Add frontend build"
git push
```

### Issue: "No data loaded" in logs

**Check:**
1. Verify JSON files are in `data/` folder
2. Make sure they're committed to Git
3. Check JSON syntax is valid

**Fix:**
```bash
# Verify data files
ls -la data/

# If missing, add them
git add data/*.json
git commit -m "Add data files"
git push
```

### Issue: "Out of memory" error

**Solutions:**
1. Reduce dataset size
2. Use smaller embedding model in `embedding.py`:
   ```python
   def __init__(self, model_name: str = "paraphrase-MiniLM-L3-v2"):
   ```
3. Upgrade to paid tier ($7/month) with more RAM

### Issue: Site is very slow

**This is normal for free tier:**
- First request after 15 minutes of inactivity takes 30-60 seconds
- Instance "wakes up" from sleep
- Subsequent requests are fast

**Solutions:**
1. Upgrade to paid tier for always-on instance
2. Use a service like UptimeRobot to ping every 10 minutes
3. Accept the cold start delay

### Issue: Frontend shows but API calls fail

**Check:**
1. Open browser DevTools (F12)
2. Check Network tab for errors
3. Look at Console for error messages

**Common causes:**
- API endpoint URL is wrong
- CORS issues
- Backend isn't running

**Fix:**
Check Render logs to ensure backend started successfully.

## Updating Your Application

### To Update Data:

```bash
# Update JSON files in data/ folder
# Then rebuild index:
rm knowledge.db faiss_index.bin id_mapping.pkl

# Commit changes
git add data/
git commit -m "Update knowledge base"
git push

# Render will auto-deploy
```

### To Update Frontend:

```bash
cd frontend
# Make changes to src/App.jsx
npm run build
cd ..

git add frontend/dist
git commit -m "Update frontend"
git push
```

### To Update Backend:

```bash
# Make changes to Python files
git add *.py
git commit -m "Update backend"
git push
```

## Cost Optimization

**Free Tier Limits:**
- 750 hours/month (always-on for one app)
- 512 MB RAM
- Shared CPU
- Spins down after 15 min inactivity

**Tips to Stay Free:**
1. Use only one web service
2. Let it spin down when not in use
3. Keep dataset under 100MB
4. Use efficient embedding model

## Next Steps

- [ ] Add more data to your knowledge base
- [ ] Customize the UI (colors, branding)
- [ ] Add authentication if needed
- [ ] Monitor usage in Render dashboard
- [ ] Share your URL with users!

## Support Resources

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: Create issue in your repo
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Congratulations! Your RAG application is now live and accessible 24/7!**

Your URL: `https://your-app-name.onrender.com`
