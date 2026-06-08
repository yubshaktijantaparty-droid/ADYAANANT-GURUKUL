import logging
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.services.leaderboard_service import LeaderboardService
from app.models.leaderboard import LeaderboardResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["leaderboard"])

@router.get(
    "/leaderboard",
    response_model=LeaderboardResponse,
    summary="Get Live Leaderboard",
    description="Retrieve the complete live leaderboard with rankings. Data is calculated in real-time from MongoDB.",
    responses={
        200: {"description": "Leaderboard retrieved successfully"},
        500: {"description": "Server error"}
    }
)
async def get_leaderboard():
    """
    Get the live leaderboard with active members and rankings.
    
    Returns:
        LeaderboardResponse: Contains active member count, leaderboard data, and timestamp
    
    Ranking Rules:
        1. Highest Points
        2. Tiebreaker: Highest Cam ON Minutes
        3. Tiebreaker: Lowest Message Count
        4. Tiebreaker: Alphabetical Username
    
    Points Calculation (Dynamic, not stored):
        points = (cam_on_minutes × 2) + (cam_off_minutes × 1) + (message_count × 1)
    """
    try:
        logger.info("Leaderboard request received")
        
        # Get leaderboard from service
        leaderboard, active_count = LeaderboardService.get_leaderboard()
        
        # Create response
        response = LeaderboardResponse(
            success=True,
            active_members=active_count,
            generated_at=datetime.utcnow(),
            leaderboard=leaderboard
        )
        
        logger.info(f"Leaderboard response: {active_count} active, {len(leaderboard)} entries")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in get_leaderboard: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve leaderboard"
        )

@router.get(
    "/member/{user_id}",
    summary="Get Member Rank",
    description="Get specific member's rank and leaderboard data.",
)
async def get_member_rank(user_id: str):
    """
    Get a specific member's rank and statistics.
    """
    try:
        logger.info(f"Member rank request for user {user_id}")
        
        result = LeaderboardService.get_member_rank(user_id)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found in leaderboard"
            )
        
        rank, entry = result
        
        return {
            "success": True,
            "rank": rank,
            "member": entry.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting member rank: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve member information"
        )

@router.get(
    "/health",
    summary="Health Check",
    description="Check API and MongoDB connectivity.",
    responses={
        200: {"description": "API is healthy"},
        503: {"description": "Service unavailable"}
    }
)
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    try:
        is_healthy = LeaderboardService.health_check()
        
        if is_healthy:
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow(),
                "mongodb": "connected"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB connection failed"
            )
            
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )
