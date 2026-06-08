# 🔱 ADYAANANT GURUKUL - Deployment Guide

## Quick Start Deployment

### For Railway Backend (5 minutes)

#### Prerequisites
- Railway Account (free tier available)
- GitHub Account
- MongoDB Atlas URI

#### Deploy Now
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Clone and navigate to backend
cd backend

# Create railway.json
echo '{}' > railway.json

# Deploy
railway up
```

#### Set Environment Variables
```bash
railway variables set MONGO_URI "your-connection-string"
```

#### Get Your URL
```bash
railway service
# Your URL: https://your-app.up.railway.app
```

---

### For GitHub Pages Frontend (2 minutes)

#### Prerequisites
- GitHub Account
- GitHub CLI (optional but recommended)

#### Deploy Steps
1. Create GitHub repository
2. Push frontend files
3. Go to Settings > Pages
4. Select main branch and /root
5. Your site: `https://username.github.io/repo-name`

---

## Environment Variables

### Backend (.env)
```
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/adyaanant_gurukul
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Frontend (js/app.js)
```javascript
const API_ENDPOINT = 'https://your-railway-app.up.railway.app/api'
```

---

## Verify Deployment

### Backend Health Check
```bash
curl https://your-app.up.railway.app/api/health
```

Response should be:
```json
{
  "status": "healthy",
  "timestamp": "2026-06-08T12:30:45",
  "mongodb": "connected"
}
```

### Leaderboard Endpoint
```bash
curl https://your-app.up.railway.app/api/leaderboard
```

### API Documentation
```
https://your-app.up.railway.app/api/docs
```

---

## Custom Domain (Optional)

### Railway with Custom Domain
1. Dashboard > Project > Project Settings
2. Add Domain
3. Enter your domain (example.com)
4. Update DNS records as shown
5. Wait for verification (usually instant)

### GitHub Pages with Custom Domain
1. Settings > Pages
2. Custom domain field
3. Enter your domain
4. Update DNS CNAME record to `username.github.io`
5. Enable HTTPS (automatic)

---

## Monitoring & Logs

### Railway Logs
```bash
railway logs -f
```

### Real-time Monitoring
```bash
# CPU & Memory usage
railway service

# Database queries
# Check MongoDB Atlas dashboard
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 502 Gateway Error | Check MongoDB connection, verify MONGO_URI |
| CORS Error | Update CORS_ORIGINS in config.py |
| Slow Requests | Check MongoDB query performance |
| Connection Timeout | Whitelist 0.0.0.0/0 in MongoDB Atlas |

---

## Cost Estimate

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Railway | $5/month | Enough for this project |
| GitHub Pages | Free | Unlimited bandwidth |
| MongoDB Atlas | Free | 512MB storage (sufficient) |
| **Total** | **$5/month** | Includes free tier services |

---

## Performance Tips

1. **Enable MongoDB Index**
   - Create index on `user_id` in user_data collection
   - Create index on `_id` in active_members collection

2. **Frontend Optimization**
   - CSS minification (production)
   - JavaScript minification (production)
   - Lazy load images if added later

3. **API Optimization**
   - 5-second polling is optimal
   - Consider caching at CDN level if needed
   - Use read replicas for MongoDB queries

---

## Security Checklist

- [ ] MONGO_URI never in code
- [ ] .env in .gitignore
- [ ] CORS configured for specific origins
- [ ] HTTPS enabled everywhere
- [ ] Read-only database user
- [ ] API rate limiting considered
- [ ] No admin passwords exposed

---

## Rollback Plan

If deployment fails:

### Railway
```bash
# View deployment history
railway history

# Rollback to previous deployment
railway redeploy --version <version-id>
```

### GitHub Pages
```bash
# Push previous version
git revert <commit>
git push origin main
```

---

## Update Deployment

### Backend Updates
```bash
# Make changes locally
# Test locally with `uvicorn main:app --reload`
# Commit and push
git add .
git commit -m "Update API"
git push origin main

# Railway auto-deploys if using GitHub integration
# Or manually deploy:
railway up
```

### Frontend Updates
```bash
# Make changes
# Commit and push
git add .
git commit -m "Update UI"
git push origin main

# GitHub Pages auto-deploys within 2-3 minutes
```

---

## Maintenance Schedule

- **Daily**: Monitor error logs
- **Weekly**: Check MongoDB query performance
- **Monthly**: Review security settings
- **Quarterly**: Update dependencies

---

**Document Version**: 1.0.0
**Last Updated**: June 2026
