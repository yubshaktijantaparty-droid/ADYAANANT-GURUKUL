# 🔱 ADYAANANT GURUKUL - Live Leaderboard Setup Guide

## Project Overview

**Status**: Production-Ready Read-Only System
**Purpose**: Display live rankings from existing Discord bot data
**Architecture**: Frontend (GitHub Pages) + Backend API (Railway) + Database (MongoDB)

---

## Part 1: MongoDB Setup

### Prerequisites
- MongoDB Atlas Account (Free tier is sufficient)
- Existing collections with data:
  - `active_members` - Contains active member information
  - `user_data` - Contains member statistics

### Connection String Format
```
mongodb+srv://username:password@cluster-name.mongodb.net/adyaanant_gurukul?retryWrites=true&w=majority
```

### Required Permissions
- **Read-Only Access** (Very important!)
- Collections: `active_members`, `user_data`

---

## Part 2: Backend Setup (Railway)

### Step 1: Prepare Backend Files
```
backend/
├── main.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
└── app/
    ├── __init__.py
    ├── config.py
    ├── db/mongodb.py
    ├── models/leaderboard.py
    ├── routers/leaderboard.py
    ├── services/leaderboard_service.py
    └── utils/logging.py
```

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Empty Project"
4. Name it "adyaanant-gurukul-api"

### Step 3: Deploy Backend

#### Option A: Using Railway CLI (Recommended)
```powershell
# Install Railway CLI
# Windows: https://railway.app/dashboard

# Login to Railway
railway login

# Navigate to backend directory
cd backend

# Create project
railway init

# Select "Deploy from current directory"
# Select "Python"

# Add MongoDB URI
railway variables set MONGO_URI "your_mongodb_uri_here"

# Deploy
railway up
```

#### Option B: GitHub Integration
1. Push code to GitHub repository
2. Connect GitHub in Railway dashboard
3. Select repository and branch
4. Set environment variables in Railway dashboard
5. Deploy

### Step 4: Configure Environment Variables
In Railway Dashboard > Variables:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/adyaanant_gurukul?retryWrites=true&w=majority
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Step 5: Verify Deployment
```
# Get your Railway URL from dashboard
# Test endpoint
curl https://your-app-domain.up.railway.app/

# Test leaderboard endpoint
curl https://your-app-domain.up.railway.app/api/leaderboard

# API documentation
https://your-app-domain.up.railway.app/api/docs
```

---

## Part 3: Frontend Setup (GitHub Pages)

### Step 1: Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. Name: `adyaanant-gurukul` or similar
3. Set to **Public** (required for GitHub Pages)

### Step 2: Upload Frontend Files
```
repository/
├── index.html
├── livelb.html
├── other.html
├── css/
│   └── style.css
├── js/
│   └── app.js
├── .gitignore
└── README.md
```

### Step 3: Configure GitHub Pages
1. Go to Repository Settings > Pages
2. Set Source to "Deploy from a branch"
3. Select main branch and /root directory
4. Save

### Step 4: Update API Endpoint in Frontend
Edit `frontend/js/app.js`:

```javascript
getApiEndpoint() {
    const hostname = window.location.hostname;
    const isDev = hostname === 'localhost' || hostname === '127.0.0.1';
    
    if (isDev) {
        return 'http://localhost:8000/api';
    }
    
    // Change this to your Railway URL
    return 'https://your-app-domain.up.railway.app/api';
}
```

### Step 5: Verify GitHub Pages Deployment
- URL: `https://yourusername.github.io/adyaanant-gurukul/`
- Wait 2-3 minutes after push for deployment
- Check Deployments tab in repository

---

## Part 4: Local Development

### Backend Setup (Windows)
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your MongoDB URI
# Then run:
$env:MONGO_URI="mongodb+srv://your_connection_string"

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (Windows)
```powershell
# Open frontend directory in VS Code
code frontend/

# Start a simple HTTP server (Python 3.10+)
python -m http.server 8080 --directory frontend

# Or using Live Server extension in VS Code
# Extensions > Live Server > Open with Live Server
```

### Testing Locally
- Frontend: `http://localhost:8080/`
- API: `http://localhost:8000/`
- API Docs: `http://localhost:8000/api/docs`

---

## Part 5: Production Checklist

### Backend (Railway)
- [ ] MongoDB URI is set in environment variables (not in code)
- [ ] DEBUG=False in production
- [ ] CORS origins configured for your domain
- [ ] All API endpoints respond correctly
- [ ] Health check endpoint returns 200
- [ ] Logs are visible in Railway dashboard
- [ ] Database read-only permissions verified

### Frontend (GitHub Pages)
- [ ] API endpoint updated to production Railway URL
- [ ] Custom domain configured (if applicable)
- [ ] HTTPS enabled (automatic with GitHub Pages)
- [ ] All pages load correctly
- [ ] Leaderboard updates every 5 seconds
- [ ] Mobile responsive design working

### Database (MongoDB)
- [ ] Connection string is secure
- [ ] Read-only user has correct permissions
- [ ] Collections are properly indexed
- [ ] Backup enabled in MongoDB Atlas

### Security
- [ ] No secrets in code
- [ ] .env file not committed to Git
- [ ] MONGO_URI only in environment variables
- [ ] No API keys exposed
- [ ] CORS properly configured

---

## Part 6: Troubleshooting

### 502 Bad Gateway (Railway)
```
Solution: Check MongoDB connection
- Verify MONGO_URI is correct
- Check MongoDB cluster connection limits
- Ensure IP whitelist includes Railway IPs (0.0.0.0/0)
```

### CORS Error on Frontend
```
Solution: Update CORS configuration
- Add GitHub Pages URL to CORS_ORIGINS in app/config.py
- Re-deploy backend
- Clear browser cache
```

### Leaderboard Not Updating
```
Solution: Check API connectivity
- Open browser DevTools (F12) > Console
- Check for network errors
- Verify API endpoint in app.js
- Ensure Railway app is running
```

### MongoDB Connection Timeout
```
Solution: Check network access
- MongoDB Atlas > Network Access
- Ensure 0.0.0.0/0 is whitelisted
- Check connection string format
```

---

## Part 7: Monitoring & Maintenance

### Railway Monitoring
- Go to Railway Dashboard > Project > Metrics
- Monitor CPU, Memory, Network
- Check logs for errors
- Set up alerts for failures

### MongoDB Monitoring
- Go to MongoDB Atlas > Metrics
- Monitor Query performance
- Check connection count
- Review replication status

### Frontend Performance
- Google Lighthouse: https://pagespeed.web.dev/
- Test mobile responsiveness
- Verify page load speed

---

## Part 8: Useful Commands

### Railway CLI Commands
```powershell
# View logs
railway logs

# View environment variables
railway variables list

# Set variable
railway variables set KEY VALUE

# Redeploy
railway redeploy

# Stop service
railway service remove
```

### MongoDB Commands (via MongoDB CLI)
```javascript
// Count active members
db.active_members.count()

// Check user data structure
db.user_data.findOne()

// List collections
show collections
```

---

## Support & Documentation

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Railway Docs**: https://docs.railway.app/
- **MongoDB Docs**: https://docs.mongodb.com/
- **GitHub Pages**: https://pages.github.com/

---

## Key Points to Remember

✅ **DO**:
- Use read-only MongoDB connections
- Store secrets in environment variables
- Update API endpoint in frontend for production
- Enable HTTPS everywhere
- Monitor API health regularly

❌ **DON'T**:
- Commit .env files
- Store data in frontend
- Create new MongoDB collections
- Modify existing documents
- Expose MongoDB URI in frontend

---

**Last Updated**: June 2026
**Version**: 1.0.0
