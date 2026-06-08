from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LeaderboardEntry(BaseModel):
    """Leaderboard entry model"""
    user_id: str
    name: str
    cam_on_minutes: int
    cam_off_minutes: int
    message_count: int
    total_points: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "1317768159494799360",
                "name": "DND...😑",
                "cam_on_minutes": 120,
                "cam_off_minutes": 60,
                "message_count": 35,
                "total_points": 265
            }
        }

class LeaderboardResponse(BaseModel):
    """Leaderboard API response model"""
    success: bool
    active_members: int
    generated_at: datetime
    leaderboard: List[LeaderboardEntry]
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "active_members": 25,
                "generated_at": "2026-06-08T12:30:45.123456",
                "leaderboard": [
                    {
                        "user_id": "1317768159494799360",
                        "name": "Top Member",
                        "cam_on_minutes": 250,
                        "cam_off_minutes": 100,
                        "message_count": 50,
                        "total_points": 650
                    }
                ]
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    details: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Database connection failed",
                "details": "Cannot connect to MongoDB"
            }
        }
