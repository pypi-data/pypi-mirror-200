from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from moontour_common.models.coordinates import Coordinates


class PhaseStatus(StrEnum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'


class Phase(BaseModel):
    target: Coordinates
    status: PhaseStatus = PhaseStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    start_time: datetime | None = None
    end_time: datetime | None
