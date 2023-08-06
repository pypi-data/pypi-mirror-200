from pydantic import BaseModel
from pydantic.color import Color

from moontour_common.models import Guess
from moontour_common.models.rooms.health_room import HealthRoom, START_HEALTH, HealthPhase
from moontour_common.models.rooms.room import RoomMode
from moontour_common.models.user import User


class Team(BaseModel):
    color: Color
    health: int = START_HEALTH
    players: list[User] = []


class TeamsPhase(HealthPhase):
    guesses: dict[str, Guess] = {}  # User ID to guess


class TeamsRoom(HealthRoom):
    @staticmethod
    def get_mode() -> RoomMode:
        return RoomMode.teams

    team_size: int = 2
    teams: dict[str, Team] = {
        'red': Team(color=Color('red')),
        'blue': Team(color=Color('blue')),
    }
    phases: list[TeamsPhase] = []
