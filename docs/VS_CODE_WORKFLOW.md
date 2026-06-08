# 🔱 ADYAANANT GURUKUL - VS Code Workflow Guide

## Opening the Project in VS Code

### Step 1: Open Workspace
```powershell
# Navigate to project folder
cd "C:\Users\prana\OneDrive\Desktop\ADG"

# Open in VS Code
code .
```

### Step 2: Workspace Structure
```
ADG/
├── frontend/              # Open in left pane
├── backend/               # Open in right pane (split view)
├── docs/                  # Documentation
└── README.md              # Main guide
```

---

## Backend Development Setup

### Terminal 1: Backend Server
```powershell
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Update MONGO_URI in .env
# Then run:
$env:MONGO_URI="mongodb+srv://your_connection"

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Testing Backend
```powershell
# In new terminal tab
# Test API
curl http://localhost:8000/

# Get leaderboard
curl http://localhost:8000/api/leaderboard

# API Documentation
# Open: http://localhost:8000/api/docs
```

---

## Frontend Development Setup

### Terminal 2: Frontend Server
```powershell
# Navigate to frontend
cd frontend

# Start HTTP server
python -m http.server 8080

# Or use Live Server extension in VS Code
# Right-click index.html > Open with Live Server
```

**Expected Output**:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

### Testing Frontend
```
Open in Browser:
- http://localhost:8080/
- http://localhost:8080/livelb.html
- http://localhost:8080/other.html
```

---

## VS Code Extensions Recommended

### Install These
1. **Python** (Microsoft)
   - Python environment management
   - Linting & debugging

2. **Pylance** (Microsoft)
   - Python type checking
   - IntelliSense

3. **Live Server** (Ritwick Dey)
   - Live reload for HTML/CSS/JS
   - Right-click > Open with Live Server

4. **Thunder Client** or **Rest Client**
   - Test API endpoints
   - View responses

5. **MongoDB for VS Code** (MongoDB)
   - Browse collections
   - Query testing

6. **Prettier** (Code Formatter)
   - Format JavaScript/HTML/CSS

### Settings (.vscode/settings.json)
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + \`` | Toggle terminal |
| `Ctrl + J` | Toggle bottom panel |
| `Ctrl + B` | Toggle sidebar |
| `Ctrl + Shift + D` | Debugging |
| `F5` | Start debugging |
| `Ctrl + F5` | Reload application |
| `Ctrl + /` | Toggle comment |
| `Alt + Shift + F` | Format document |

---

## Debugging

### Python Backend Debugging
1. Click on line number to set breakpoint
2. Press F5 to start debugging
3. Use Debug Console to inspect variables
4. Step through code with F10/F11

### JavaScript Frontend Debugging
1. Press F12 to open DevTools
2. Sources tab to set breakpoints
3. Step through code
4. Console for logging

---

## File Editing Tips

### Backend Files
```
app/config.py            - Update configuration
app/db/mongodb.py        - MongoDB connection
app/models/leaderboard.py - Data models
app/services/*.py        - Business logic
app/routers/*.py         - API endpoints
main.py                  - FastAPI app entry
```

### Frontend Files
```
index.html              - Home page structure
livelb.html            - Leaderboard page
css/style.css          - All styling
js/app.js              - Live polling logic
other.html             - Coming soon page
```

---

## Common Workflows

### Adding a New API Endpoint
1. Create function in `app/routers/leaderboard.py`
2. Add route decorator `@router.get("/endpoint")`
3. Add response model if needed
4. Test with Thunder Client
5. Update frontend if consuming

### Updating UI Design
1. Edit `frontend/css/style.css`
2. Live Server auto-refreshes
3. Check responsive design
4. Test on mobile/tablet

### Database Schema Changes (Read-Only)
❌ **NOT ALLOWED** - This is strictly read-only

---

## Running Tasks

### Create tasks.json
1. Ctrl + Shift + B to open tasks
2. Create tasks for:
   - Start Backend Server
   - Start Frontend Server
   - Run Tests

### Example tasks.json
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Backend: Start Server",
      "type": "shell",
      "command": "cd backend && uvicorn main:app --reload",
      "group": "build",
      "isBackground": true
    },
    {
      "label": "Frontend: Start Server",
      "type": "shell",
      "command": "cd frontend && python -m http.server 8080",
      "group": "build",
      "isBackground": true
    }
  ]
}
```

---

## Git Workflow

### Initial Setup
```powershell
# Initialize git
git init

# Create .gitignore (already created)

# Add all files
git add .

# Commit
git commit -m "Initial project setup"

# Create GitHub repo
# Add remote
git remote add origin https://github.com/yourusername/adyaanant-gurukul.git

# Push
git branch -M main
git push -u origin main
```

### Regular Workflow
```powershell
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main
```

---

## Environment Setup Checklist

### First Time Setup
- [ ] Clone/download project
- [ ] Create backend/.env from .env.example
- [ ] Set MONGO_URI in .env
- [ ] Create virtual environment (`python -m venv venv`)
- [ ] Activate venv (`.\venv\Scripts\Activate.ps1`)
- [ ] Install requirements (`pip install -r requirements.txt`)
- [ ] Start backend server (`uvicorn main:app --reload`)
- [ ] Start frontend server (`python -m http.server 8080`)
- [ ] Open http://localhost:8080 in browser

### Daily Development
- [ ] Activate backend venv
- [ ] Start backend server
- [ ] Start frontend server
- [ ] Check http://localhost:8080/livelb.html loads data
- [ ] Review any error logs

---

## Performance Monitoring

### Monitor Backend
- Terminal: Check uvicorn output
- Browser: http://localhost:8000/api/docs
- DevTools: Network tab for API calls

### Monitor Frontend
- Browser DevTools
- Network tab (API calls every 5 seconds)
- Console tab (check for errors)
- Lighthouse: Performance audit

### Monitor Database
- MongoDB Atlas dashboard
- Connection status
- Query performance

---

## Troubleshooting

### Backend Won't Start
```
Error: Address already in use
Solution: 
  netstat -ano | findstr :8000
  taskkill /PID <pid> /F
```

### Cannot Find Module
```
Error: ModuleNotFoundError
Solution:
  Make sure venv is activated
  pip install -r requirements.txt
```

### CORS Error in Frontend
```
Error: Access to XMLHttpRequest blocked by CORS
Solution:
  Check CORS settings in app/config.py
  Add localhost to CORS_ORIGINS
  Restart backend
```

### MongoDB Connection Failed
```
Error: Failed to connect to MongoDB
Solution:
  Verify MONGO_URI in .env
  Check network connectivity
  Verify IP whitelist in MongoDB Atlas
```

---

## Useful Commands

### Python Venv
```powershell
# Create
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Deactivate
deactivate

# Install packages
pip install -r requirements.txt

# Freeze requirements
pip freeze > requirements.txt
```

### MongoDB CLI
```bash
# Connect to MongoDB
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/adyaanant_gurukul"

# Show databases
show dbs

# Use database
use adyaanant_gurukul

# Show collections
show collections

# Count documents
db.active_members.count()

# Find one record
db.user_data.findOne()
```

---

## Best Practices

### Code Organization
- Keep files focused and small
- Use meaningful function names
- Add docstrings to functions
- Comment complex logic

### Frontend
- Use semantic HTML
- Mobile-first CSS design
- Avoid hardcoded URLs (use config)
- Test across browsers

### Backend
- Keep endpoints simple
- Use descriptive error messages
- Log important events
- Validate all inputs

### Database
- Never modify data (read-only!)
- Use indexes for performance
- Monitor query performance
- Keep connections pooled

---

## Documentation

- **README.md** - Project overview
- **docs/SETUP.md** - Detailed setup guide
- **docs/DEPLOYMENT.md** - Production deployment
- **docs/API_DOCUMENTATION.md** - API reference

---

## Next Steps

1. ✅ Open project in VS Code
2. ✅ Set up backend virtual environment
3. ✅ Configure MongoDB URI
4. ✅ Start backend server
5. ✅ Start frontend server
6. ✅ Test application
7. ✅ Deploy to production

---

**Happy coding! 🔱**

*Excellence Through Community*
