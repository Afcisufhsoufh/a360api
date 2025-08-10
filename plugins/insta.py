# Copyright @ISmartCoder
# Updates Channel: https://t.me/TheSmartDev
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlparse, parse_qs, unquote
from utils import LOGGER

router = APIRouter(prefix="/insta")
API_URL = "https://fastdl.live/api/search"
HEADERS = {"Content-Type": "application/json"}

def extract_filename(download_url, index):
    parsed = urlparse(download_url)
    query = parse_qs(parsed.query)
    return unquote(query.get('filename', [f"media_{index}"])[0])

@router.get("/dl")
async def download(url: str = ""):
    if not url:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error": "Missing 'url' parameter",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    
    payload = {"url": url}
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        if response.status_code != 200:
            LOGGER.error(f"API request failed for URL {url}: HTTP {response.status_code}")
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "error": f"API request failed: HTTP {response.status_code}",
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev"
                }
            )
        
        data = response.json()
        if not data.get("success") or not data.get("result"):
            LOGGER.error(f"No media found or invalid URL: {url}")
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "error": "No media found or invalid URL",
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev"
                }
            )
        
        media_list = data['result']
        for index, item in enumerate(media_list, 1):
            item['filename'] = extract_filename(item['downloadLink'], index)
        
        return JSONResponse(
            content={
                "status": "success",
                "media_count": len(media_list),
                "results": media_list,
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    
    except Exception as e:
        LOGGER.error(f"Unexpected error for URL {url}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e),
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )