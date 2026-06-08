# 🔱 ADYAANANT GURUKUL - Local Setup Guide

Complete guide to running the website locally on your machine.

---

## ✅ Quick Start (Windows)

### Option 1: Automated Script (Recommended)
```powershell
cd c:\Users\prana\OneDrive\Desktop\ADG
.\start-local.ps1
```

This script will:
- ✓ Stop any existing servers on ports 8000 and 8001
- ✓ Install Python dependencies
- ✓ Start the backend API on `http://127.0.0.1:8000`
- ✓ Start the frontend server on `http://127.0.0.1:8001`
- ✓ Automatically open the live leaderboard in your browser

---

### Option 2: Manual Setup

#### Step 1: Start Backend
```powershell
cd c:\Users\prana\OneDrive\Desktop\ADG\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 2: Start Frontend (new PowerShell window)
```powershell
cd c:\Users\prana\OneDrive\Desktop\ADG\frontend
python -m http.server 8001
```

#### Step 3: Open in Browser
- Homepage: `http://127.0.0.1:8001/index.html`
- Live Leaderboard: `http://127.0.0.1:8001/livelb.html`

---

## 📍 Important: Use 127.0.0.1, NOT 0.0.0.0

❌ **DON'T use:** `http://0.0.0.0:8001/`  
✅ **DO use:** `http://127.0.0.1:8001/`

The `0.0.0.0` address is a server binding address, not a valid client URL.

---

## 🌐 Local URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend (Index) | `http://127.0.0.1:8001/index.html` | Homepage with navigation |
| Frontend (Leaderboard) | `http://127.0.0.1:8001/livelb.html` | Live leaderboard display |
| Backend API | `http://127.0.0.1:8000` | API root |
| API Leaderboard | `http://127.0.0.1:8000/api/leaderboard` | Get leaderboard data |
| API Health | `http://127.0.0.1:8000/api/health` | Health check |
| API Docs | `http://127.0.0.1:8000/api/docs` | Swagger UI documentation |

---

## ✨ Features Working Locally

- ✓ Homepage with animated title and navigation
- ✓ Live leaderboard with real-time API polling (5 second updates)
- ✓ Active member count display
- ✓ Timestamp updates
- ✓ Live/Offline status indicator
- ✓ Empty state messaging when no data available
- ✓ Responsive design on all screen sizes
- ✓ CORS handling for local development

---

## 📊 Data Flow (Local)

```
Browser (127.0.0.1:8001)
    ↓
Frontend JS (app.js)
    ↓
API Request (http://127.0.0.1:8000/api/leaderboard)
    ↓
Backend FastAPI (main:app)
    ↓
MongoDB Atlas (Read-Only)
    ↓
Response: JSON Leaderboard Data
    ↓
Browser Renders Table & Updates Timestamp
```

---

## 🔧 Troubleshooting

### Port 8000/8001 Already in Use
```powershell
# Kill process using port 8000
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force

# Kill process using port 8001
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001).OwningProcess -Force
```

### Virtual Environment Not Activated
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### MongoDB Connection Error
- Ensure `.env` file in `backend/` contains valid `MONGO_URI`
- Check MongoDB Atlas credentials
- Verify IP whitelist includes your current IP

### Frontend Shows "No leaderboard data available"
- This is normal if there are no active members in the database
- API returns: `"active_members": 0`
- The UI gracefully handles empty data

### "Connection Offline" Status
- Check that backend is running on port 8000
- Verify API is responding: `curl http://127.0.0.1:8000/api/health`
- Check browser console (F12 → Console tab) for errors

---

## 🚀 Production Deployment

### Backend (Railway)
1. Deploy backend to Railway (see `docs/DEPLOYMENT.md`)
2. Set `MONGO_URI` environment variable in Railway
3. Note your Railway URL: `https://your-app.up.railway.app`

### Frontend (GitHub Pages)
- Frontend files are automatically deployed to `docs/` folder
- GitHub Pages serves from: `https://yubshaktijantaparty-droid.github.io/ADYAANANT-GURUKUL/`
- Production endpoint configured in `frontend/js/app.js`

---

## 📚 Additional Resources

- **API Docs**: `http://127.0.0.1:8000/api/docs` (Swagger UI)
- **Setup Guide**: `docs/SETUP.md`
- **Deployment Guide**: `docs/DEPLOYMENT.md`
- **API Reference**: `docs/API_DOCUMENTATION.md`

---

## 🎯 Expected Behavior

### Homepage (index.html)
- Shows animated "ADYAANANT GURUKUL" title
- Two navigation buttons:
  - 🏆 LIVE LEADERBOARD → Navigate to leaderboard
  - 📌 OTHER → Coming soon page

### Live Leaderboard (livelb.html)
- Fetches data every 5 seconds
- Shows active member count
- Updates timestamp in real-time
- Displays connection status (Live/Offline)
- Shows either:
  - Leaderboard table with rankings (if data exists)
  - "No leaderboard data available" message (if empty)

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-08  
**Status**: ✅ Fully Functional
