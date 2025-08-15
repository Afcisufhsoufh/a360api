from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import aiohttp
import asyncio
from typing import List

router = APIRouter(prefix="/tera")
API_KEY = "oPpT1SUjPzraqDq_sI2-pKiSFUGjOtm08mtN81G_bs876gwQIcrieyoDhyCnHHrN"
API_URL = "https://debrid-link.com/api/v2/downloader/add"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def generate_download_link(terabox_url: str, password: str = None):
    payload = {"url": terabox_url}
    if password:
        payload["password"] = password
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.post(API_URL, json=payload, timeout=10) as response:
                response_data = await response.json()
                result = {
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev",
                    "response": response_data,
                    "is_password_protected": bool(password)
                }
                if response.status == 200 and response_data.get("success", False):
                    download_url = response_data.get("value", {}).get("downloadUrl")
                    result["download_url"] = download_url if download_url else "No download link returned"
                else:
                    result["error"] = response_data.get("error", "Unknown error")
                return result
    except aiohttp.ClientConnectionError as e:
        return {
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev",
            "error": f"Connection error: {str(e)}",
            "is_password_protected": bool(password)
        }
    except aiohttp.ClientResponseError as e:
        return {
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev",
            "error": f"API request failed: {str(e)}",
            "is_password_protected": bool(password)
        }
    except asyncio.TimeoutError:
        return {
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev",
            "error": "Request timed out",
            "is_password_protected": bool(password)
        }
    except Exception as e:
        return {
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev",
            "error": f"Unexpected error: {str(e)}",
            "is_password_protected": bool(password)
        }

@router.get("/dl")
async def download_terabox_links(url: List[str] = Query(...)):
    if not url:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "At least one URL is required",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )

    tasks = [generate_download_link(u) for u in url]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return JSONResponse(
        content={
            "success": True,
            "results": results,
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev"
        }
    )
