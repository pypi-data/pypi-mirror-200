from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float
    heading: float | None
    pitch: float | None
