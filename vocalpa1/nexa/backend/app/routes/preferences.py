"""
User preferences routes
Mirrors Android SharedPreferences and Web localStorage functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, Union

from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class PreferenceRequest(BaseModel):
    key: str
    value: Union[str, int, float, bool, dict, list]
    value_type: Optional[str] = None


class PreferenceResponse(BaseModel):
    key: str
    value: Union[str, int, float, bool, dict, list]
    value_type: str


@router.get("/", response_model=Dict[str, Any])
async def get_all_preferences(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get all user preferences"""
    repos = RepositoryFactory(db)
    preferences = repos.preferences.get_all_preferences(user_id)
    return preferences


@router.get("/{key}")
async def get_preference(
    key: str,
    default: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get specific preference value"""
    repos = RepositoryFactory(db)
    value = repos.preferences.get_preference(user_id, key, default)
    
    return {
        "key": key,
        "value": value,
        "exists": value is not None
    }


@router.post("/", response_model=PreferenceResponse)
async def set_preference(
    request: PreferenceRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Set preference value"""
    try:
        repos = RepositoryFactory(db)
        repos.preferences.set_preference(
            user_id, 
            request.key, 
            request.value, 
            request.value_type
        )
        
        # Determine actual value type
        if request.value_type is None:
            if isinstance(request.value, bool):
                value_type = "boolean"
            elif isinstance(request.value, (int, float)):
                value_type = "number"
            elif isinstance(request.value, (dict, list)):
                value_type = "json"
            else:
                value_type = "string"
        else:
            value_type = request.value_type
        
        return PreferenceResponse(
            key=request.key,
            value=request.value,
            value_type=value_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set preference: {str(e)}")


@router.delete("/{key}")
async def delete_preference(
    key: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Delete preference"""
    try:
        repos = RepositoryFactory(db)
        repos.preferences.delete_preference(user_id, key)
        
        return {"success": True, "message": f"Preference '{key}' deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete preference: {str(e)}")


@router.post("/batch")
async def set_multiple_preferences(
    preferences: Dict[str, Any],
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Set multiple preferences at once"""
    try:
        repos = RepositoryFactory(db)
        
        for key, value in preferences.items():
            repos.preferences.set_preference(user_id, key, value)
        
        return {
            "success": True,
            "message": f"Set {len(preferences)} preferences",
            "keys": list(preferences.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set preferences: {str(e)}")


@router.get("/defaults/app")
async def get_default_app_preferences():
    """Get default application preferences"""
    return {
        "theme": "light",
        "language": "en-US",
        "voice_enabled": True,
        "wake_word_enabled": True,
        "wake_word_sensitivity": 0.5,
        "tts_speed": 1.0,
        "tts_voice": "default",
        "background_listening": True,
        "notification_sounds": True,
        "auto_launch": False,
        "privacy_mode": False,
        "data_collection": True,
        "crash_reporting": True
    }


@router.get("/defaults/voice")
async def get_default_voice_preferences():
    """Get default voice-related preferences"""
    return {
        "wake_words": ["nexa", "hey nexa", "ok nexa"],
        "voice_timeout": 5,
        "speech_language": "en-US",
        "tts_language": "en-US",
        "voice_feedback": True,
        "beep_on_activation": True,
        "continuous_listening": False,
        "noise_suppression": True,
        "echo_cancellation": True
    }


@router.post("/reset")
async def reset_preferences(
    category: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Reset preferences to defaults"""
    try:
        repos = RepositoryFactory(db)
        
        if category == "app":
            defaults = await get_default_app_preferences()
        elif category == "voice":
            defaults = await get_default_voice_preferences()
        else:
            # Reset all to defaults
            app_defaults = await get_default_app_preferences()
            voice_defaults = await get_default_voice_preferences()
            defaults = {**app_defaults, **voice_defaults}
        
        # Set all default preferences
        for key, value in defaults.items():
            repos.preferences.set_preference(user_id, key, value)
        
        return {
            "success": True,
            "message": f"Reset {len(defaults)} preferences to defaults",
            "category": category or "all"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset preferences: {str(e)}")


@router.get("/export")
async def export_preferences(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Export all user preferences"""
    repos = RepositoryFactory(db)
    preferences = repos.preferences.get_all_preferences(user_id)
    
    return {
        "user_id": user_id,
        "preferences": preferences,
        "exported_at": "2024-01-01T00:00:00Z",  # Use actual timestamp
        "version": "1.0"
    }


@router.post("/import")
async def import_preferences(
    preferences_data: Dict[str, Any],
    overwrite: bool = False,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Import preferences from exported data"""
    try:
        repos = RepositoryFactory(db)
        
        if "preferences" not in preferences_data:
            raise HTTPException(status_code=400, detail="Invalid preferences data format")
        
        preferences = preferences_data["preferences"]
        imported_count = 0
        
        for key, value in preferences.items():
            # Check if preference exists if not overwriting
            if not overwrite:
                existing = repos.preferences.get_preference(user_id, key)
                if existing is not None:
                    continue  # Skip existing preferences
            
            repos.preferences.set_preference(user_id, key, value)
            imported_count += 1
        
        return {
            "success": True,
            "message": f"Imported {imported_count} preferences",
            "total_available": len(preferences),
            "overwrite_mode": overwrite
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import preferences: {str(e)}")
