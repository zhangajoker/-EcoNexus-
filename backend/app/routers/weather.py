"""Weather proxy (moved from main.py). Falls back to fixed values when the
upstream request fails, as before."""

import httpx
from fastapi import APIRouter

from app.config import WEATHER_URL

router = APIRouter(prefix="/api", tags=["weather"])


@router.get("/weather")
async def get_weather_data():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(WEATHER_URL, timeout=10.0)
            res.raise_for_status()
            return res.json()
    except Exception:
        return {"current": {"temperature_2m": 24.5, "relative_humidity_2m": 60, "weather_code": 1},
                "status": "fallback"}
