import logging
from typing import List, Dict, Any
from datetime import datetime
from app.db.mongodb import mongodb_manager
from app.models.leaderboard import LeaderboardEntry

logger = logging.getLogger(__name__)

class LeaderboardService:
    """
    Leaderboard Service - Handles all leaderboard logic
    READ-ONLY: Only fetches and calculates data, never modifies MongoDB
    """
    
    @staticmethod
    def calculate_points(cam_on_minutes: int, cam_off_minutes: int, message_count: int) -> int:
        """
        Calculate total points - Dynamic calculation (no storage)
        Formula: (cam_on_minutes × 2) + (cam_off_minutes × 1) + (message_count × 1)
        """
        return (cam_on_minutes * 2) + cam_off_minutes + message_count
    
    @classmethod
    def get_leaderboard(cls) -> tuple[List[LeaderboardEntry], int]:
        """
        Get complete leaderboard with ranking
        
        Returns:
            - List of LeaderboardEntry objects (sorted by ranking rules)
            - Count of active members
        
        Ranking Rules:
            1. Highest Points
            2. Tiebreaker: Highest Cam ON Minutes
            3. Tiebreaker: Lowest Message Count
            4. Tiebreaker: Alphabetical Username
        """
        try:
            logger.info("Fetching leaderboard data...")
            
            # Get collections
            active_members_collection = mongodb_manager.get_active_members_collection()
            user_data_collection = mongodb_manager.get_user_data_collection()
            
            # Count active members
            active_count = active_members_collection.count_documents({})
            logger.info(f"Active members: {active_count}")
            
            # Get all active member IDs
            active_members = active_members_collection.find({}, {"_id": 1, "name": 1})
            active_members_dict = {str(member["_id"]): member.get("name", "Unknown") for member in active_members}
            
            if not active_members_dict:
                logger.warning("No active members found")
                return [], active_count
            
            # Build leaderboard
            leaderboard_entries = []
            
            for user_id, name in active_members_dict.items():
                try:
                    # Get user data
                    user_data = user_data_collection.find_one({"_id": int(user_id)})
                    
                    if not user_data:
                        logger.debug(f"No data found for user {user_id}")
                        # Create entry with default values
                        cam_on = 0
                        cam_off = 0
                        messages = 0
                    else:
                        # Extract metrics from user data
                        cam_on = user_data.get("voice_cam_on_minutes", 0)
                        cam_off = user_data.get("voice_cam_off_minutes", 0)
                        messages = user_data.get("data", {}).get("message_count", 0)
                    
                    # Calculate points dynamically
                    points = cls.calculate_points(cam_on, cam_off, messages)
                    
                    # Create leaderboard entry
                    entry = LeaderboardEntry(
                        user_id=user_id,
                        name=name,
                        cam_on_minutes=cam_on,
                        cam_off_minutes=cam_off,
                        message_count=messages,
                        total_points=points
                    )
                    
                    leaderboard_entries.append(entry)
                    
                except Exception as e:
                    logger.error(f"Error processing user {user_id}: {str(e)}")
                    continue
            
            # Sort by ranking rules
            leaderboard_entries.sort(key=lambda x: (
                -x.total_points,                    # 1. Highest Points (descending)
                -x.cam_on_minutes,                  # 2. Highest Cam ON Minutes (descending)
                x.message_count,                    # 3. Lowest Message Count (ascending)
                x.name.lower()                      # 4. Alphabetical Username (ascending)
            ))
            
            logger.info(f"Leaderboard generated: {len(leaderboard_entries)} entries")
            
            return leaderboard_entries, active_count
            
        except Exception as e:
            logger.error(f"Error generating leaderboard: {str(e)}", exc_info=True)
            raise
    
    @classmethod
    def get_member_rank(cls, user_id: str) -> tuple[int, LeaderboardEntry] | None:
        """
        Get specific member's rank and data
        """
        try:
            leaderboard, _ = cls.get_leaderboard()
            
            for rank, entry in enumerate(leaderboard, 1):
                if entry.user_id == user_id:
                    return rank, entry
            
            logger.warning(f"Member {user_id} not found in leaderboard")
            return None
            
        except Exception as e:
            logger.error(f"Error getting member rank: {str(e)}")
            raise
    
    @classmethod
    def health_check(cls) -> bool:
        """
        Health check - Verify MongoDB connectivity
        """
        try:
            return mongodb_manager.health_check()
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
