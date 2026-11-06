from fastapi import APIRouter, HTTPException, Query

from app.schemas.geo import GeocodeOut, RouteOut
from app.services.geo import geocode, route_distance

router = APIRouter()


@router.get("/geocode", response_model=GeocodeOut)
def geocode_endpoint(q: str = Query(min_length=3, max_length=300)):
    result = geocode(q)
    if not result:
        raise HTTPException(status_code=404, detail="Endereco nao encontrado")
    return result


@router.get("/route", response_model=RouteOut)
def route_endpoint(
    from_lat: float = Query(ge=-90, le=90),
    from_lon: float = Query(ge=-180, le=180),
    to_lat: float = Query(ge=-90, le=90),
    to_lon: float = Query(ge=-180, le=180),
):
    return route_distance(from_lat, from_lon, to_lat, to_lon)
