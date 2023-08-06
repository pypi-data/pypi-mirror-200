from moontour_common.models import Guess
from moontour_common.models.rooms.health_room import HealthRoom, START_HEALTH, HealthPhase
from moontour_common.models.rooms.room import RoomMode
from moontour_common.models.user import User


class DuelPlayer(User):
    health: int = START_HEALTH


class DuelPhase(HealthPhase):
    guesses: dict[str, Guess] = {}  # User ID to guess


class DuelRoom(HealthRoom):
    @staticmethod
    def get_mode() -> RoomMode:
        return RoomMode.duel

    player_count: int = 2
    players: list[DuelPlayer] = []
    phases: list[DuelPhase] = []
