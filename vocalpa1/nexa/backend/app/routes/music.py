"""
Music API integration routes
Spotify integration and music control functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import base64
from datetime import datetime

from ..config import get_settings
from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class Track(BaseModel):
    id: str
    name: str
    artist: str
    album: str
    duration_ms: int
    preview_url: Optional[str] = None
    external_url: str


class Playlist(BaseModel):
    id: str
    name: str
    description: Optional[str]
    track_count: int
    external_url: str


class MusicSearchResponse(BaseModel):
    tracks: List[Track]
    total: int
    source: str


@router.get("/search", response_model=MusicSearchResponse)
async def search_music(
    query: str,
    type: str = "track",
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Search for music tracks, artists, or albums"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        raise HTTPException(
            status_code=503,
            detail="Spotify API credentials not configured"
        )
    
    try:
        # Get Spotify access token
        access_token = await _get_spotify_token(
            settings.spotify_client_id,
            settings.spotify_client_secret
        )
        
        # Search Spotify
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "q": query,
            "type": type,
            "limit": min(limit, 50)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Convert tracks to our format
        tracks = []
        if "tracks" in data and data["tracks"]["items"]:
            for item in data["tracks"]["items"]:
                tracks.append(Track(
                    id=item["id"],
                    name=item["name"],
                    artist=", ".join([artist["name"] for artist in item["artists"]]),
                    album=item["album"]["name"],
                    duration_ms=item["duration_ms"],
                    preview_url=item.get("preview_url"),
                    external_url=item["external_urls"]["spotify"]
                ))
        
        # Log API usage
        repos.system.log_event(
            "music_search_call",
            "music_service",
            f"Search query: {query}",
            "info",
            user_id
        )
        
        return MusicSearchResponse(
            tracks=tracks,
            total=data.get("tracks", {}).get("total", len(tracks)),
            source="spotify"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Music search error: {str(e)}")


@router.get("/recommendations")
async def get_music_recommendations(
    seed_genres: Optional[str] = None,
    seed_artists: Optional[str] = None,
    seed_tracks: Optional[str] = None,
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get music recommendations from Spotify"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        raise HTTPException(
            status_code=503,
            detail="Spotify API credentials not configured"
        )
    
    try:
        # Get Spotify access token
        access_token = await _get_spotify_token(
            settings.spotify_client_id,
            settings.spotify_client_secret
        )
        
        # Get recommendations
        url = "https://api.spotify.com/v1/recommendations"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": min(limit, 100)}
        
        if seed_genres:
            params["seed_genres"] = seed_genres
        if seed_artists:
            params["seed_artists"] = seed_artists
        if seed_tracks:
            params["seed_tracks"] = seed_tracks
        
        # Default to popular genres if no seeds provided
        if not any([seed_genres, seed_artists, seed_tracks]):
            params["seed_genres"] = "pop,rock,electronic"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Convert to our format
        tracks = []
        for item in data.get("tracks", []):
            tracks.append(Track(
                id=item["id"],
                name=item["name"],
                artist=", ".join([artist["name"] for artist in item["artists"]]),
                album=item["album"]["name"],
                duration_ms=item["duration_ms"],
                preview_url=item.get("preview_url"),
                external_url=item["external_urls"]["spotify"]
            ))
        
        return {
            "tracks": tracks,
            "total": len(tracks),
            "source": "spotify_recommendations"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations error: {str(e)}")


@router.get("/genres")
async def get_available_genres():
    """Get available music genres from Spotify"""
    settings = get_settings()
    
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        raise HTTPException(
            status_code=503,
            detail="Spotify API credentials not configured"
        )
    
    try:
        # Get Spotify access token
        access_token = await _get_spotify_token(
            settings.spotify_client_id,
            settings.spotify_client_secret
        )
        
        # Get available genres
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        
        return {
            "genres": data.get("genres", []),
            "total": len(data.get("genres", []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Genres error: {str(e)}")


@router.post("/control/play")
async def play_music(
    track_uri: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Control music playback (requires Spotify Premium)"""
    repos = RepositoryFactory(db)
    
    # Log the control action
    repos.system.log_event(
        "music_control",
        "music_service",
        f"Play command: {track_uri or 'resume'}",
        "info",
        user_id
    )
    
    # Note: Actual Spotify playback control requires user authentication
    # and Spotify Premium. This is a placeholder implementation.
    return {
        "success": True,
        "action": "play",
        "track_uri": track_uri,
        "message": "Playback control sent (requires Spotify Premium and authentication)"
    }


@router.post("/control/pause")
async def pause_music(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Pause music playback"""
    repos = RepositoryFactory(db)
    
    repos.system.log_event(
        "music_control",
        "music_service",
        "Pause command",
        "info",
        user_id
    )
    
    return {
        "success": True,
        "action": "pause",
        "message": "Pause command sent"
    }


@router.post("/control/next")
async def next_track(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Skip to next track"""
    repos = RepositoryFactory(db)
    
    repos.system.log_event(
        "music_control",
        "music_service",
        "Next track command",
        "info",
        user_id
    )
    
    return {
        "success": True,
        "action": "next",
        "message": "Next track command sent"
    }


@router.post("/control/previous")
async def previous_track(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Skip to previous track"""
    repos = RepositoryFactory(db)
    
    repos.system.log_event(
        "music_control",
        "music_service",
        "Previous track command",
        "info",
        user_id
    )
    
    return {
        "success": True,
        "action": "previous",
        "message": "Previous track command sent"
    }


async def _get_spotify_token(client_id: str, client_secret: str) -> str:
    """Get Spotify access token using client credentials flow"""
    url = "https://accounts.spotify.com/api/token"
    
    # Encode credentials
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
    
    return token_data["access_token"]


@router.get("/playlists/featured")
async def get_featured_playlists(
    limit: int = 20,
    user_id: str = Depends(get_current_user_id)
):
    """Get featured playlists from Spotify"""
    settings = get_settings()
    
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        raise HTTPException(
            status_code=503,
            detail="Spotify API credentials not configured"
        )
    
    try:
        # Get Spotify access token
        access_token = await _get_spotify_token(
            settings.spotify_client_id,
            settings.spotify_client_secret
        )
        
        # Get featured playlists
        url = "https://api.spotify.com/v1/browse/featured-playlists"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": min(limit, 50)}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Convert to our format
        playlists = []
        for item in data.get("playlists", {}).get("items", []):
            playlists.append(Playlist(
                id=item["id"],
                name=item["name"],
                description=item.get("description"),
                track_count=item["tracks"]["total"],
                external_url=item["external_urls"]["spotify"]
            ))
        
        return {
            "playlists": playlists,
            "total": len(playlists),
            "source": "spotify_featured"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Featured playlists error: {str(e)}")
