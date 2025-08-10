from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from smartbindb import SmartBinDB
from utils import LOGGER

router = APIRouter(prefix="/bindb")
smartdb = SmartBinDB()

@router.get("/bin")
async def get_bin_info(country: str = None, bank: str = None, num: str = None, amount: int = 1000):
    try:
        if num:
            result = await smartdb.get_bin_info(num)
            if not result:
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": "No information found for the provided BIN",
                        "api_owner": "@ISmartCoder",
                        "api_updates": "t.me/TheSmartDev"
                    }
                )
            result["api_owner"] = "@ISmartCoder"
            result["api_updates"] = "t.me/TheSmartDev"
            return JSONResponse(content=result)
        
        elif country:
            country_code = country.upper()
            if country_code == "UK":
                country_code = "GB"
            results = await smartdb.get_bins_by_country(country_code, amount)
            if not results:
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": f"No BINs found for country code {country_code}",
                        "api_owner": "@ISmartCoder",
                        "api_updates": "t.me/TheSmartDev"
                    }
                )
            response = {
                "results": results,
                "total_results": len(results),
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
            return JSONResponse(content=response)
        
        elif bank:
            results = await smartdb.get_bins_by_bank(bank, amount)
            if not results:
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": f"No BINs found for bank {bank}",
                        "api_owner": "@ISmartCoder",
                        "api_updates": "t.me/TheSmartDev"
                    }
                )
            response = {
                "results": results,
                "total_results": len(results),
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
            return JSONResponse(content=response)
        
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "At least one of country, bank, or num parameters is required",
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev"
                }
            )
    
    except ValueError as e:
        LOGGER.error(f"Invalid input for BIN lookup: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "error": str(e),
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )
    except Exception as e:
        LOGGER.error(f"Error processing BIN request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }
        )