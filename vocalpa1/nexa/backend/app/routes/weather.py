"""
Weather API integration routes
Supports OpenWeatherMap and WeatherAPI services
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
from datetime import datetime

from ..config import get_settings
from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class WeatherRequest(BaseModel):
    location: str
    units: str = "metric"  # metric, imperial, kelvin


class WeatherResponse(BaseModel):
    location: str
    current: Dict[str, Any]
    forecast: Optional[Dict[str, Any]] = None
    source: str
    timestamp: datetime


@router.get("/current")
async def get_current_weather(
    location: str,
    units: str = "metric",
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get current weather for location"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    try:
        # Try OpenWeatherMap first
        if settings.openweather_api_key:
            weather_data = await _get_openweather_current(
                location, units, settings.openweather_api_key
            )
            source = "openweathermap"
        elif settings.weatherapi_key:
            weather_data = await _get_weatherapi_current(
                location, units, settings.weatherapi_key
            )
            source = "weatherapi"
        else:
            raise HTTPException(
                status_code=503, 
                detail="No weather API key configured"
            )
        
        # Log API usage
        repos.system.log_event(
            "weather_api_call",
            "weather_service",
            f"Weather request for {location}",
            "info",
            user_id
        )
        
        return WeatherResponse(
            location=location,
            current=weather_data,
            source=source,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")


@router.get("/forecast")
async def get_weather_forecast(
    location: str,
    days: int = 5,
    units: str = "metric",
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get weather forecast for location"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    try:
        if settings.openweather_api_key:
            current_data = await _get_openweather_current(
                location, units, settings.openweather_api_key
            )
            forecast_data = await _get_openweather_forecast(
                location, units, settings.openweather_api_key, days
            )
            source = "openweathermap"
        elif settings.weatherapi_key:
            current_data = await _get_weatherapi_current(
                location, units, settings.weatherapi_key
            )
            forecast_data = await _get_weatherapi_forecast(
                location, units, settings.weatherapi_key, days
            )
            source = "weatherapi"
        else:
            raise HTTPException(
                status_code=503,
                detail="No weather API key configured"
            )
        
        # Log API usage
        repos.system.log_event(
            "weather_forecast_call",
            "weather_service", 
            f"Forecast request for {location} ({days} days)",
            "info",
            user_id
        )
        
        return WeatherResponse(
            location=location,
            current=current_data,
            forecast=forecast_data,
            source=source,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather forecast error: {str(e)}")


async def _get_openweather_current(location: str, units: str, api_key: str) -> Dict[str, Any]:
    """Get current weather from OpenWeatherMap"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    
    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"].get("deg"),
        "visibility": data.get("visibility"),
        "uv_index": None  # Not available in current weather
    }


async def _get_openweather_forecast(location: str, units: str, api_key: str, days: int) -> Dict[str, Any]:
    """Get forecast from OpenWeatherMap"""
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": units,
        "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    
    # Process forecast data
    daily_forecasts = []
    for item in data["list"][:days]:
        daily_forecasts.append({
            "date": item["dt_txt"],
            "temperature": {
                "min": item["main"]["temp_min"],
                "max": item["main"]["temp_max"]
            },
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
            "humidity": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"]
        })
    
    return {"daily": daily_forecasts}


async def _get_weatherapi_current(location: str, units: str, api_key: str) -> Dict[str, Any]:
    """Get current weather from WeatherAPI"""
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": location,
        "aqi": "yes"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    
    current = data["current"]
    
    # Convert temperature based on units
    temp = current["temp_c"] if units == "metric" else current["temp_f"]
    feels_like = current["feelslike_c"] if units == "metric" else current["feelslike_f"]
    wind_speed = current["wind_kph"] if units == "metric" else current["wind_mph"]
    
    return {
        "temperature": temp,
        "feels_like": feels_like,
        "humidity": current["humidity"],
        "pressure": current["pressure_mb"],
        "description": current["condition"]["text"],
        "icon": current["condition"]["icon"],
        "wind_speed": wind_speed,
        "wind_direction": current["wind_degree"],
        "visibility": current["vis_km"] if units == "metric" else current["vis_miles"],
        "uv_index": current["uv"]
    }


async def _get_weatherapi_forecast(location: str, units: str, api_key: str, days: int) -> Dict[str, Any]:
    """Get forecast from WeatherAPI"""
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": min(days, 10),  # WeatherAPI supports up to 10 days
        "aqi": "no"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    
    # Process forecast data
    daily_forecasts = []
    for day in data["forecast"]["forecastday"]:
        day_data = day["day"]
        
        # Convert temperatures based on units
        min_temp = day_data["mintemp_c"] if units == "metric" else day_data["mintemp_f"]
        max_temp = day_data["maxtemp_c"] if units == "metric" else day_data["maxtemp_f"]
        
        daily_forecasts.append({
            "date": day["date"],
            "temperature": {
                "min": min_temp,
                "max": max_temp
            },
            "description": day_data["condition"]["text"],
            "icon": day_data["condition"]["icon"],
            "humidity": day_data["avghumidity"],
            "wind_speed": day_data["maxwind_kph"] if units == "metric" else day_data["maxwind_mph"],
            "chance_of_rain": day_data["daily_chance_of_rain"],
            "uv_index": day_data["uv"]
        })
    
    return {"daily": daily_forecasts}


@router.get("/locations/search")
async def search_locations(
    query: str,
    limit: int = 5,
    user_id: str = Depends(get_current_user_id)
):
    """Search for weather locations"""
    settings = get_settings()
    
    try:
        if settings.weatherapi_key:
            url = "http://api.weatherapi.com/v1/search.json"
            params = {
                "key": settings.weatherapi_key,
                "q": query
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                locations = response.json()
            
            return {
                "locations": locations[:limit],
                "source": "weatherapi"
            }
        else:
            # Fallback to a simple response
            return {
                "locations": [{"name": query, "country": "Unknown"}],
                "source": "fallback"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Location search error: {str(e)}")
