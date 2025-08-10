# Copyright @ISmartCoder
# Updates Channel: https://t.me/TheSmartDev
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import aiohttp
from utils import LOGGER
import pytz
import pycountry
from datetime import datetime

router = APIRouter(prefix="/sk")
STRIPE_URL = "https://api.stripe.com/v1/account"

async def verify_stripe_key(stripe_key: str):
    headers = {"Authorization": f"Bearer {stripe_key}"}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(STRIPE_URL, timeout=10) as response:
                return response.status == 200
    except Exception as e:
        LOGGER.error(f"Error verifying Stripe key: {str(e)}")
        return False

async def get_stripe_key_info(stripe_key: str):
    headers = {"Authorization": f"Bearer {stripe_key}"}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(STRIPE_URL, timeout=10) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return {
                    "id": data.get("id", "N/A"),
                    "email": data.get("email", "N/A"),
                    "country": data.get("country", "N/A"),
                    "business_name": data.get("business_name", "N/A"),
                    "type": data.get("type", "N/A"),
                    "payouts_enabled": data.get("payouts_enabled", "N/A"),
                    "details_submitted": data.get("details_submitted", "N/A")
                }
    except Exception as e:
        LOGGER.error(f"Error fetching Stripe key info: {str(e)}")
        return None

def get_flag(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if not country:
            return None, "Unknown"
        country_name = country.name
        flag_emoji = ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper())
        if not all(0x1F1E6 <= ord(c) <= 0x1F1FF for c in flag_emoji):
            return country_name, "Unknown"
        return country_name, flag_emoji
    except Exception as e:
        LOGGER.error(f"Error in get_flag: {str(e)}")
        return None, "Unknown"

async def get_time_and_calendar(country_input: str):
    country_code = None
    try:
        country_input = country_input.lower().strip()
        if country_input in ["uk", "united kingdom"]:
            country_code = "gb"
        elif country_input in ["uae", "united arab emirates"]:
            country_code = "ae"
        else:
            try:
                country = pycountry.countries.search_fuzzy(country_input)[0]
                country_code = country.alpha_2
            except LookupError:
                country_code = country_input.upper().strip()
                if len(country_code) != 2 or not pycountry.countries.get(alpha_2=country_code):
                    raise ValueError("Invalid country code or name")
        country_name, flag_emoji = get_flag(country_code)
        if not country_name:
            country_name = "Unknown"
        time_zones = {
            "gb": ["Europe/London"],
            "ae": ["Asia/Dubai"]
        }.get(country_code, pytz.country_timezones.get(country_code))
        if time_zones:
            tz = pytz.timezone(time_zones[0])
            now = datetime.now(tz)
            time_str = now.strftime("%I:%M:%S %p")
            date_str = now.strftime("%d %b, %Y")
            day_str = now.strftime("%A")
            timezone = time_zones[0]
        else:
            now = datetime.now()
            time_str = "00:00:00 AM"
            date_str = "Unknown Date"
            day_str = "Unknown Day"
            timezone = "Unknown"
        return {
            "country_name": country_name,
            "country_code": country_code,
            "time": time_str,
            "date": date_str,
            "day": day_str,
            "timezone": timezone,
            "flag": flag_emoji
        }
    except ValueError as e:
        LOGGER.error(f"ValueError in get_time_and_calendar: {str(e)}")
        return None
    except Exception as e:
        LOGGER.error(f"Unexpected error in get_time_and_calendar: {str(e)}")
        return None

@router.get("/chk")
async def check_stripe_key(key: str = ""):
    if not key:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Missing 'key' parameter",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    try:
        is_live = await verify_stripe_key(key)
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "status": "Live" if is_live else "Dead"
                },
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error verifying Stripe key: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )

@router.get("/info")
async def get_stripe_key_details(key: str = ""):
    if not key:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Missing 'key' parameter",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    try:
        data = await get_stripe_key_info(key)
        if data is None:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Invalid Stripe key or API error",
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev"
                }
            )
        return JSONResponse(
            content={
                "success": True,
                "data": data,
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error fetching Stripe key info: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )

@router.get("/time")
async def get_country_time(country: str = ""):
    if not country:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Missing 'country' parameter",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    try:
        data = await get_time_and_calendar(country)
        if data is None:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Invalid country code or name",
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev"
                }
            )
        return JSONResponse(
            content={
                "success": True,
                "data": data,
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error fetching time for country {country}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )