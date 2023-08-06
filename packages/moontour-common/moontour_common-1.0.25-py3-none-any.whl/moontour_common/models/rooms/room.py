import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, validator


class RoomMode(StrEnum):
    streak = 'streak'
    duel = 'duel'
    teams = 'teams'


class RoomStatus(StrEnum):
    waiting = 'waiting'
    waiting_to_start = 'waitingToStart'
    running = 'running'
    closed = 'closed'


class BaseRoom(BaseModel):
    id: str = Field(alias='id_', default_factory=lambda: str(uuid.uuid4()))
    map: str = 'world'
    status: RoomStatus = RoomStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    start_time: datetime | None = None
    mode: RoomMode | None = None

    @validator("mode", always=True)
    def compute_mode(cls, value):
        return cls.get_mode() or value

    @staticmethod
    def get_mode() -> RoomMode | None:
        return None

    class Config:
        allow_population_by_field_name = True
