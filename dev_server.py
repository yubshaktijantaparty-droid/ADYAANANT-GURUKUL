#!/usr/bin/env python
"""
Unified development server for ADYAANANT GURUKUL
Serves both frontend (static files) and backend API from the same port
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.utils.logging import setup_logging
from app.db.mongodb import mongodb_manager
from app.routers import leaderboard
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Define paths
frontend_path = Path(__file__).parent / "frontend"

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("=" * 60)
    logger.info("🔱 ADYAANANT GURUKUL - Development Server Starting...")
    logger.info("=" * 60)
    logger.info(f"Version: {settings.API_VERSION}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"Database: {settings.MONGO_DB_NAME}")
    
    # Verify MongoDB connection
    try:
        if not mongodb_manager.health_check():
            logger.error("✗ Failed to connect to MongoDB")
            raise Exception("MongoDB connection failed")
        logger.info("✓ MongoDB connection verified")
    except Exception as e:
        logger.error(f"✗ Startup failed: {str(e)}")
        raise
    
    logger.info("✓ Development server started successfully")
    logger.info("=" * 60)
    logger.info(f"Frontend: http://localhost:8000")
    logger.info(f"API Docs: http://localhost:8000/api/docs")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("🔱 ADYAANANT GURUKUL - Development Server Shutting Down...")
    logger.info("=" * 60)
    mongodb_manager.close_connection()
    logger.info("✓ Server stopped")
    logger.info("=" * 60)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS Middleware - allow all for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers FIRST (before catch-all routes)
app.include_router(leaderboard.router, prefix="/api")

# Mount static files (frontend assets)
app.mount("/static", StaticFiles(directory=str(frontend_path / "assets")), name="static")

# Root endpoint - serve index.html
@app.get("/")
async def root():
    """Serve index.html for root path"""
    return FileResponse(path=str(frontend_path / "index.html"))

# Serve other HTML files and catch-all
@app.get("/{file_path:path}")
async def serve_files(file_path: str):
    """Serve frontend static files and pages"""
    # Reject API paths (they should be handled by the router above)
    if file_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Build the requested file path
    requested_path = frontend_path / file_path
    
    # Check if it's a real file
    if requested_path.exists() and requested_path.is_file():
        return FileResponse(path=str(requested_path))
    
    # Try adding .html extension
    html_path = frontend_path / f"{file_path}.html"
    if html_path.exists():
        return FileResponse(path=str(html_path))
    
    # Default to index.html for SPA (Single Page Application) routing
    if not any(file_path.endswith(ext) for ext in ['.css', '.js', '.json', '.png', '.jpg', '.gif', '.ico', '.svg', '.woff', '.woff2']):
        return FileResponse(path=str(frontend_path / "index.html"))
    
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    
    uvicorn.run(
        "dev_server:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=["backend", "frontend"]
    )
