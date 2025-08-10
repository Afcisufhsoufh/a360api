# Copyright @ISmartCoder
# Updates Channel: https://t.me/TheSmartDev
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from datetime import datetime
from utils import LOGGER

router = APIRouter(prefix="/thrd")

@router.get("/dl")
async def download_video(url: str = ""):
    if not url:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Missing 'url' parameter",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev",
                "timestamp": datetime.now().isoformat(),
                "message": "Please provide a valid Threads URL"
            }
        )
    
    api_url = "https://api.threadsphotodownloader.com/v2/media"
    params = {"url": url}
    
    try:
        response = requests.get(api_url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            videos = data.get("video_urls", [])
            if videos:
                return JSONResponse(
                    content={
                        "success": True,
                        "video_url": videos[0]["download_url"],
                        "video_quality": videos[0].get("quality", "HD"),
                        "file_size": videos[0].get("file_size", "Unknown"),
                        "api_owner": "@ISmartCoder",
                        "api_updates": "t.me/TheSmartDev",
                        "timestamp": datetime.now().isoformat(),
                        "message": "Video downloaded successfully",
                        "total_videos_found": len(videos),
                        "server_response_time": f"{response.elapsed.total_seconds():.2f}s"
                    }
                )
            else:
                return JSONResponse(
                    status_code=404,
                    content={
                        "success": False,
                        "error": "No video found in post",
                        "api_owner": "@ISmartCoder",
                        "api_updates": "t.me/TheSmartDev",
                        "timestamp": datetime.now().isoformat(),
                        "message": "The provided URL doesn't contain any downloadable videos"
                    }
                )
        else:
            LOGGER.error(f"External API returned status {response.status_code} for URL {url}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "External API Error",
                    "status_code": response.status_code,
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Failed to fetch video from external service"
                }
            )
    
    except requests.exceptions.Timeout:
        LOGGER.error(f"Request timeout for URL {url}")
        return JSONResponse(
            status_code=408,
            content={
                "success": False,
                "error": "Request timeout",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev",
                "timestamp": datetime.now().isoformat(),
                "message": "The request took too long to process"
            }
        )
    
    except Exception as e:
        LOGGER.error(f"Unexpected error for URL {url}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev",
                "timestamp": datetime.now().isoformat(),
                "message": "An unexpected error occurred"
            }
        )