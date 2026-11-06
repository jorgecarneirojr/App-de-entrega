import math
import time
from typing import Any

import httpx
from app.core.config import settings

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

_GEOCODE_CACHE_TTL_SECONDS = 24 * 60 * 60
_ROUTE_CACHE_TTL_SECONDS = 5 * 60
_geocode_cache: dict[str, tuple[float, dict[str, Any] | None]] = {}
_route_cache: dict[str, tuple[float, dict[str, Any]]] = {}


def _read_cache(cache: dict[str, tuple[float, Any]], key: str, ttl: int) -> Any | None:
    entry = cache.get(key)
    if not entry:
        return None
    created_at, value = entry
    if time.monotonic() - created_at > ttl:
        cache.pop(key, None)
        return None
    return value


def _write_cache(cache: dict[str, tuple[float, Any]], key: str, value: Any) -> None:
    if len(cache) > 512:
        cache.clear()
    cache[key] = (time.monotonic(), value)


def _value(source: Any, key: str) -> Any:
    if isinstance(source, dict):
        return source.get(key)
    return getattr(source, key, None)


def build_address_query(address: Any) -> str:
    parts = [
        _value(address, "street"),
        _value(address, "number"),
        _value(address, "district"),
        _value(address, "city"),
        _value(address, "state"),
        _value(address, "zip_code"),
        "Brasil",
    ]
    return ", ".join(str(part).strip() for part in parts if part)


def geocode(query: str) -> dict[str, Any] | None:
    query = " ".join(query.split())
    if not query:
        return None

    cached = _read_cache(_geocode_cache, query, _GEOCODE_CACHE_TTL_SECONDS)
    if cached is not None:
        return cached

    try:
        response = httpx.get(
            NOMINATIM_URL,
            params={
                "q": query,
                "format": "jsonv2",
                "limit": 1,
                "countrycodes": "br",
                "addressdetails": 0,
            },
            headers={"User-Agent": settings.GEOCODING_USER_AGENT},
            timeout=settings.GEOCODING_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        results = response.json()
        result = {
            "latitude": float(results[0]["lat"]),
            "longitude": float(results[0]["lon"]),
            "display_name": results[0].get("display_name"),
        } if results else None
    except (httpx.HTTPError, ValueError, KeyError, IndexError):
        result = None

    _write_cache(_geocode_cache, query, result)
    return result


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * radius_km * math.asin(math.sqrt(a))


def route_distance(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
) -> dict[str, Any]:
    key = f"{from_lat:.5f},{from_lon:.5f};{to_lat:.5f},{to_lon:.5f}"
    cached = _read_cache(_route_cache, key, _ROUTE_CACHE_TTL_SECONDS)
    if cached is not None:
        return cached

    try:
        response = httpx.get(
            f"{OSRM_URL}/{from_lon},{from_lat};{to_lon},{to_lat}",
            params={"overview": "full", "geometries": "geojson", "steps": "false"},
            headers={"User-Agent": settings.GEOCODING_USER_AGENT},
            timeout=settings.GEOCODING_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        route = data["routes"][0]
        coordinates = route["geometry"]["coordinates"]
        result = {
            "distance_km": round(route["distance"] / 1000, 2),
            "duration_min": max(1, round(route["duration"] / 60)),
            "geometry": [[float(lat), float(lon)] for lon, lat in coordinates],
            "source": "osrm",
        }
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError):
        distance = haversine_km(from_lat, from_lon, to_lat, to_lon) * 1.3
        result = {
            "distance_km": round(distance, 2),
            "duration_min": max(1, round(distance / 30 * 60)),
            "geometry": [[from_lat, from_lon], [to_lat, to_lon]],
            "source": "estimado",
        }

    _write_cache(_route_cache, key, result)
    return result
