from pydantic import BaseModel


class GeocodeOut(BaseModel):
    latitude: float
    longitude: float
    display_name: str | None = None


class RouteOut(BaseModel):
    distance_km: float
    duration_min: int
    geometry: list[list[float]]
    source: str
