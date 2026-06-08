import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.config import settings
from app.utils.logging import setup_logging
from app.db.mongodb import mongodb_manager
from app.routers import leaderboard

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("=" * 60)
    logger.info("🔱 ADYAANANT GURUKUL - Live Leaderboard API Starting...")
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
    
    logger.info("✓ API started successfully")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("🔱 ADYAANANT GURUKUL - Live Leaderboard API Shutting Down...")
    logger.info("=" * 60)
    mongodb_manager.close_connection()
    logger.info("✓ API stopped")
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

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],  # Read-only methods
    allow_headers=["Content-Type", "Accept"],
    expose_headers=["Content-Type"],
    max_age=3600,
)

# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Include routers
app.include_router(leaderboard.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "ADYAANANT GURUKUL Live Leaderboard API",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/api/docs",
        "endpoints": {
            "leaderboard": "/api/leaderboard",
            "member": "/api/member/{user_id}",
            "health": "/api/health"
        }
    }

# API root
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "name": "Live Leaderboard API",
        "version": settings.API_VERSION,
        "description": "Read-only API for ADYAANANT GURUKUL live rankings",
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/leaderboard",
                "description": "Get complete live leaderboard"
            },
            {
                "method": "GET",
                "path": "/api/member/{user_id}",
                "description": "Get specific member's rank"
            },
            {
                "method": "GET",
                "path": "/api/health",
                "description": "Health check"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(settings.__dict__.get("PORT", 8000))
    host = settings.__dict__.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
