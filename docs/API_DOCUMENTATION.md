# 🔱 ADYAANANT GURUKUL - API Documentation

## API Overview

**Base URL**: `https://your-app.up.railway.app/api`  
**Version**: 1.0.0  
**Authentication**: None (Read-only, public API)  
**Rate Limit**: None (Railway limits apply)

---

## Response Format

All responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-06-08T12:30:45.123456",
  "error": null
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message here",
  "details": "Additional error details"
}
```

---

## Endpoints

### 1. Get Leaderboard

**Endpoint**: `GET /api/leaderboard`

**Description**: Retrieve the complete live leaderboard with all active members ranked.

**Parameters**: None

**Response**: 
```json
{
  "success": true,
  "active_members": 25,
  "generated_at": "2026-06-08T12:30:45.123456",
  "leaderboard": [
    {
      "user_id": "1317768159494799360",
      "name": "DND...😑",
      "cam_on_minutes": 250,
      "cam_off_minutes": 100,
      "message_count": 50,
      "total_points": 650
    },
    {
      "user_id": "1460654283794944195",
      "name": "Active Member",
      "cam_on_minutes": 120,
      "cam_off_minutes": 60,
      "message_count": 35,
      "total_points": 335
    }
  ]
}
```

**HTTP Status**: 200 (Success), 500 (Server Error)

**Ranking Algorithm**:
```
Primary: Highest total_points (descending)
├─ Tiebreaker 1: Highest cam_on_minutes (descending)
├─ Tiebreaker 2: Lowest message_count (ascending)
└─ Tiebreaker 3: Name alphabetical (ascending)
```

**Points Calculation** (Dynamic, not stored):
```
total_points = (cam_on_minutes × 2) + (cam_off_minutes × 1) + (message_count × 1)

Example:
  cam_on_minutes: 120
  cam_off_minutes: 60
  message_count: 35
  
  total_points = (120 × 2) + 60 + 35 = 240 + 60 + 35 = 335
```

**Example Request**:
```bash
curl -X GET "https://your-app.up.railway.app/api/leaderboard" \
  -H "Accept: application/json"
```

**Frontend Integration**:
```javascript
const response = await fetch('https://your-api.app/api/leaderboard');
const data = await response.json();

if (data.success) {
  console.log(`Active Members: ${data.active_members}`);
  console.log(`Leaderboard has ${data.leaderboard.length} entries`);
}
```

---

### 2. Get Member Rank

**Endpoint**: `GET /api/member/{user_id}`

**Description**: Get a specific member's rank and statistics.

**Parameters**:
- `user_id` (path, required): Discord user ID as string

**Response**:
```json
{
  "success": true,
  "rank": 1,
  "member": {
    "user_id": "1317768159494799360",
    "name": "DND...😑",
    "cam_on_minutes": 250,
    "cam_off_minutes": 100,
    "message_count": 50,
    "total_points": 650
  }
}
```

**HTTP Status**: 
- 200 (Found)
- 404 (Member not in leaderboard)
- 500 (Server Error)

**Example Request**:
```bash
curl -X GET "https://your-app.up.railway.app/api/member/1317768159494799360" \
  -H "Accept: application/json"
```

**Error Response** (404):
```json
{
  "success": false,
  "error": "Member not found in leaderboard"
}
```

---

### 3. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check API and MongoDB connectivity. Use for monitoring.

**Parameters**: None

**Response** (Healthy):
```json
{
  "status": "healthy",
  "timestamp": "2026-06-08T12:30:45",
  "mongodb": "connected"
}
```

**Response** (Unhealthy):
```json
{
  "status": "unhealthy",
  "timestamp": "2026-06-08T12:30:45",
  "mongodb": "disconnected",
  "error": "MongoDB connection failed"
}
```

**HTTP Status**: 
- 200 (Healthy)
- 503 (Service Unavailable)

**Example Request**:
```bash
curl -X GET "https://your-app.up.railway.app/api/health"
```

**Monitoring Integration**:
```javascript
// Check every minute
setInterval(async () => {
  const response = await fetch('https://your-api.app/api/health');
  const data = await response.json();
  
  if (response.status === 200) {
    console.log('✓ API is healthy');
  } else {
    console.log('✗ API is down');
    // Send alert
  }
}, 60000);
```

---

### 4. Root Endpoint

**Endpoint**: `GET /`

**Description**: API information and available endpoints.

**Response**:
```json
{
  "name": "ADYAANANT GURUKUL Live Leaderboard API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/api/docs",
  "endpoints": {
    "leaderboard": "/api/leaderboard",
    "member": "/api/member/{user_id}",
    "health": "/api/health"
  }
}
```

---

### 5. API Docs

**Endpoint**: `GET /api/docs`

**Description**: Interactive API documentation (Swagger UI)

**Access**: https://your-app.up.railway.app/api/docs

**Features**:
- Test all endpoints
- View request/response schemas
- Download OpenAPI spec

---

## Data Models

### LeaderboardEntry
```json
{
  "user_id": "1317768159494799360",
  "name": "Member Name",
  "cam_on_minutes": 250,
  "cam_off_minutes": 100,
  "message_count": 50,
  "total_points": 650
}
```

### LeaderboardResponse
```json
{
  "success": true,
  "active_members": 25,
  "generated_at": "2026-06-08T12:30:45.123456",
  "leaderboard": [
    // LeaderboardEntry objects
  ]
}
```

---

## Error Codes

| HTTP Status | Error | Meaning |
|-------------|-------|---------|
| 200 | - | Success |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Member not found |
| 500 | Internal Server Error | Database or server error |
| 503 | Service Unavailable | Database connection failed |

---

## Rate Limiting

Currently, no rate limiting is implemented. However, it's recommended that:
- Frontend polls every 5 seconds maximum
- Avoid hammering the API with requests
- Use reasonable caching if many requests needed

---

## CORS Support

The API supports CORS requests from:
- `http://localhost:*` (Development)
- `https://*.github.io` (GitHub Pages)
- Custom domains (configured in environment)

**Allowed Methods**: GET, OPTIONS  
**Allowed Headers**: Content-Type, Accept  
**Credentials**: Not allowed (read-only API)

---

## Performance Considerations

### Response Times
- Average: 100-200ms
- Maximum: 500ms (with MongoDB latency)
- Network dependent

### Database Queries
- Leaderboard query: Reads all active members + user data
- Optimized with MongoDB indexing
- No write operations (read-only)

### Recommended Polling Interval
- **Frontend**: 5 seconds (default)
- **Monitoring**: 1-5 minutes
- **Health checks**: 1 minute

---

## Example Usage

### JavaScript / Frontend
```javascript
class LeaderboardAPI {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async getLeaderboard() {
    const response = await fetch(`${this.baseUrl}/leaderboard`);
    return await response.json();
  }

  async getMember(userId) {
    const response = await fetch(`${this.baseUrl}/member/${userId}`);
    if (response.status === 404) {
      throw new Error('Member not found');
    }
    return await response.json();
  }

  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.status === 200;
  }
}

// Usage
const api = new LeaderboardAPI('https://your-app.up.railway.app/api');

// Get leaderboard
const leaderboard = await api.getLeaderboard();
console.log(`${leaderboard.active_members} members`);

// Get specific member
const member = await api.getMember('1317768159494799360');
console.log(`Rank: ${member.rank}`);
```

### Python / Backend
```python
import requests

BASE_URL = "https://your-app.up.railway.app/api"

# Get leaderboard
response = requests.get(f"{BASE_URL}/leaderboard")
data = response.json()

if data['success']:
    print(f"Active members: {data['active_members']}")
    for entry in data['leaderboard'][:5]:
        print(f"#{entry['rank']} - {entry['name']}: {entry['total_points']} pts")

# Get member rank
response = requests.get(f"{BASE_URL}/member/1317768159494799360")
data = response.json()

if data['success']:
    print(f"Rank: {data['rank']}")
```

### cURL
```bash
# Get leaderboard
curl https://your-app.up.railway.app/api/leaderboard

# Pretty print
curl https://your-app.up.railway.app/api/leaderboard | python -m json.tool

# Get specific member
curl https://your-app.up.railway.app/api/member/1317768159494799360

# Health check
curl https://your-app.up.railway.app/api/health
```

---

## Changelog

### Version 1.0.0 (June 2026)
- Initial release
- Leaderboard endpoint
- Member rank endpoint
- Health check endpoint
- Full CORS support
- API documentation

---

## Support

For issues or questions:
1. Check API documentation: `/api/docs`
2. Review this guide
3. Check Railway logs
4. Verify MongoDB connection

---

**API Documentation Version**: 1.0.0  
**Last Updated**: June 2026
