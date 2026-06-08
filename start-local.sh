#!/bin/bash
# Start ADYAANANT GURUKUL locally

echo "🔱 Starting ADYAANANT GURUKUL Local Development Server..."
echo ""

# Kill any existing processes on ports 8000 and 8001
echo "Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true

# Start Backend
echo "Starting Backend API on http://localhost:8000..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Frontend
echo "Starting Frontend on http://localhost:8001..."
cd ../frontend
python -m http.server 8001 > /dev/null 2>&1 &
FRONTEND_PID=$!

echo ""
echo "✅ Development servers started!"
echo ""
echo "Frontend: http://localhost:8001"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Keep script running
wait
