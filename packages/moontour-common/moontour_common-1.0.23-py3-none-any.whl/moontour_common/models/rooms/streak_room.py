from moontour_common.models.guess import Guess
from moontour_common.models.phase import Phase
from moontour_common.models.rooms.room import BaseRoom, RoomMode
from moontour_common.models.user import User


class StreaksPhase(Phase):
    guess: Guess | None = None


class StreakRoom(BaseRoom):
    @staticmethod
    def get_mode() -> RoomMode:
        return RoomMode.streak

    streak: int = 0
    phases: list[StreaksPhase] = []
    player: User | None
