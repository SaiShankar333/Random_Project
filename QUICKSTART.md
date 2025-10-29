# Quick Start Guide

## Get the system running in 5 minutes

### Step 1: Start Backend (Terminal 1)

```bash
cd "/Users/saishankars/Desktop/SIP II/Shivani's Project/backend"
python3 app.py
```

You should see:
```
Fake Review Detection API Server
Starting server on http://localhost:5000
```

### Step 2: Start Frontend (Terminal 2)

```bash
cd "/Users/saishankars/Desktop/SIP II/Shivani's Project/frontend"
npm run dev
```

You should see:
```
VITE ready in XXXms
Local: http://localhost:5173
```

### Step 3: Open Browser

Navigate to: **http://localhost:5173**

## Test the System

### Option 1: Use Detector Page

1. Click "Detector" in navbar
2. Click "Load Fake Example" button
3. Click "Analyze Review"
4. See the fake review prediction!

### Option 2: Use Dashboard

1. Click "Dashboard" in navbar
2. View analytics and charts
3. Explore review statistics

### Option 3: Upload Bulk Reviews

1. Click "Bulk Analysis" in navbar
2. Download template CSV
3. Upload the template file
4. Download results with predictions

## Stopping the Application

### Terminal 1 (Backend):
Press `Ctrl + C`

### Terminal 2 (Frontend):
Press `Ctrl + C`

## Common Issues

**"Model not found" error?**
```bash
cd ml_models
python3 train_model.py
```

**Port already in use?**
Kill the process or change ports in config files.

**Dependencies missing?**
```bash
# Backend
pip3 install Flask flask-cors pandas numpy scikit-learn nltk joblib

# Frontend
cd frontend
npm install
```

---

That's it! You now have a fully functional fake review detection system running locally.

