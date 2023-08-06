from moontour_common.models import Phase
from moontour_common.models.rooms.room import BaseRoom

START_HEALTH = 5000


class HealthRoom(BaseRoom):
    start_health = START_HEALTH
    guess_duration: float = 15  # Time between first guess to phase ending


class HealthPhase(Phase):
    damage_multiplier: float = 1
