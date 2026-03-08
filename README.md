# AI Mental Health Assessment System

## 🚀 Deploy to Internet (Free) — Render.com

Anyone on any network can access your app permanently.

### Step 1 — Push to GitHub
1. Go to https://github.com and create a free account
2. Click "New Repository" → name it `mental-health-app` → Create
3. Download GitHub Desktop from https://desktop.github.com
4. Open GitHub Desktop → Add your project folder
5. Commit and Push to GitHub

### Step 2 — Deploy on Render
1. Go to https://render.com → Sign up free (use GitHub login)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Fill in these settings:
   - Name: mental-health-app
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
5. Click "Create Web Service"
6. Wait 2-3 minutes → you get a FREE permanent URL like:
   https://mental-health-app.onrender.com

Share that URL with ANYONE in the WORLD! 🌍

---

## 💻 Run Locally (same WiFi only)
```bash
pip install -r requirements.txt
python app.py
```
Access at: http://YOUR_IP:5000

---

## 📁 Project Structure
```
mental_health_app/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── Procfile               # For cloud deployment
├── model/model.pkl        # Trained KNN model
├── dataset/               # Training data
├── templates/             # HTML pages
└── static/                # CSS and JS
```
