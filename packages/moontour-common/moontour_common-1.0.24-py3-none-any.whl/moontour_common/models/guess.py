from datetime import datetime

import geopy.distance
from pydantic import BaseModel, Field, validator

from moontour_common.models import Coordinates

MAX_POINTS = 5000


class Guess(BaseModel):
    time: datetime = Field(default_factory=datetime.now)
    coordinates: Coordinates
    target: Coordinates
    distance: float | None
    points: int | None

    @validator('distance', always=True)
    def compute_distance(cls, v, values):
        guess = values['coordinates']
        target = values['target']
        return geopy.distance.geodesic(
            (target.latitude, target.longitude),
            (guess.latitude, guess.longitude)
        ).km

    @validator('points', always=True)
    def compute_points(cls, v, values):
        distance = values['distance']
        if distance is None:
            return None
        return max(MAX_POINTS - int(distance), 0)
