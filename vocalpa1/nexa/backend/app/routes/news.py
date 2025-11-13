"""
News API integration routes
Fetches news from NewsAPI and other sources
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
from datetime import datetime, timedelta

from ..config import get_settings
from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory
from .auth import get_current_user_id

router = APIRouter()


class NewsArticle(BaseModel):
    title: str
    description: Optional[str]
    url: str
    source: str
    published_at: datetime
    image_url: Optional[str] = None
    category: Optional[str] = None


class NewsResponse(BaseModel):
    articles: List[NewsArticle]
    total_results: int
    source: str
    timestamp: datetime


@router.get("/headlines", response_model=NewsResponse)
async def get_top_headlines(
    country: str = "us",
    category: Optional[str] = None,
    page_size: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get top news headlines"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    if not settings.newsapi_key:
        raise HTTPException(
            status_code=503,
            detail="News API key not configured"
        )
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": settings.newsapi_key,
            "country": country,
            "pageSize": min(page_size, 100)
        }
        
        if category:
            params["category"] = category
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Convert to our format
        articles = []
        for article in data.get("articles", []):
            if article["title"] and article["url"]:
                articles.append(NewsArticle(
                    title=article["title"],
                    description=article.get("description"),
                    url=article["url"],
                    source=article["source"]["name"],
                    published_at=datetime.fromisoformat(
                        article["publishedAt"].replace("Z", "+00:00")
                    ),
                    image_url=article.get("urlToImage"),
                    category=category
                ))
        
        # Log API usage
        repos.system.log_event(
            "news_api_call",
            "news_service",
            f"Headlines request: {country}/{category}",
            "info",
            user_id
        )
        
        return NewsResponse(
            articles=articles,
            total_results=data.get("totalResults", len(articles)),
            source="newsapi",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News API error: {str(e)}")


@router.get("/search", response_model=NewsResponse)
async def search_news(
    query: str,
    language: str = "en",
    sort_by: str = "publishedAt",
    page_size: int = 20,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Search news articles"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    if not settings.newsapi_key:
        raise HTTPException(
            status_code=503,
            detail="News API key not configured"
        )
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": settings.newsapi_key,
            "q": query,
            "language": language,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100)
        }
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Convert to our format
        articles = []
        for article in data.get("articles", []):
            if article["title"] and article["url"]:
                articles.append(NewsArticle(
                    title=article["title"],
                    description=article.get("description"),
                    url=article["url"],
                    source=article["source"]["name"],
                    published_at=datetime.fromisoformat(
                        article["publishedAt"].replace("Z", "+00:00")
                    ),
                    image_url=article.get("urlToImage")
                ))
        
        # Log API usage
        repos.system.log_event(
            "news_search_call",
            "news_service",
            f"Search query: {query}",
            "info",
            user_id
        )
        
        return NewsResponse(
            articles=articles,
            total_results=data.get("totalResults", len(articles)),
            source="newsapi",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News search error: {str(e)}")


@router.get("/categories")
async def get_news_categories():
    """Get available news categories"""
    return {
        "categories": [
            "business",
            "entertainment", 
            "general",
            "health",
            "science",
            "sports",
            "technology"
        ]
    }


@router.get("/sources")
async def get_news_sources(
    country: Optional[str] = None,
    category: Optional[str] = None,
    language: str = "en"
):
    """Get available news sources"""
    settings = get_settings()
    
    if not settings.newsapi_key:
        raise HTTPException(
            status_code=503,
            detail="News API key not configured"
        )
    
    try:
        url = "https://newsapi.org/v2/sources"
        params = {
            "apiKey": settings.newsapi_key,
            "language": language
        }
        
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        return {
            "sources": data.get("sources", []),
            "total": len(data.get("sources", []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sources API error: {str(e)}")


@router.get("/trending")
async def get_trending_topics(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get trending news topics (simplified implementation)"""
    settings = get_settings()
    repos = RepositoryFactory(db)
    
    # Get recent popular searches from command history
    try:
        # This is a simplified trending implementation
        # In production, you'd use more sophisticated trending algorithms
        trending_queries = [
            "technology",
            "politics", 
            "sports",
            "entertainment",
            "business",
            "health",
            "science"
        ]
        
        trending_articles = []
        
        if settings.newsapi_key:
            # Get a few articles for each trending topic
            for query in trending_queries[:3]:  # Limit to avoid API rate limits
                try:
                    url = "https://newsapi.org/v2/everything"
                    params = {
                        "apiKey": settings.newsapi_key,
                        "q": query,
                        "sortBy": "popularity",
                        "pageSize": 2,
                        "language": "en"
                    }
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, params=params)
                        if response.status_code == 200:
                            data = response.json()
                            for article in data.get("articles", [])[:1]:  # Take top article
                                if article["title"] and article["url"]:
                                    trending_articles.append({
                                        "title": article["title"],
                                        "source": article["source"]["name"],
                                        "url": article["url"],
                                        "topic": query
                                    })
                except:
                    continue  # Skip failed requests
        
        return {
            "trending_topics": trending_queries,
            "trending_articles": trending_articles,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trending topics error: {str(e)}")


@router.get("/summary")
async def get_news_summary(
    category: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    """Get a brief news summary"""
    try:
        # Get top 5 headlines
        headlines_response = await get_top_headlines(
            category=category,
            page_size=5,
            user_id=user_id,
            db=db
        )
        
        # Create summary
        summary_items = []
        for article in headlines_response.articles[:3]:
            summary_items.append({
                "headline": article.title,
                "source": article.source,
                "time": article.published_at.strftime("%H:%M")
            })
        
        return {
            "summary": summary_items,
            "category": category or "general",
            "total_articles": headlines_response.total_results,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News summary error: {str(e)}")
