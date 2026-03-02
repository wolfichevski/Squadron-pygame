import random
from settings import SET
from entities.powerups import ShieldPowerUp, ShrinkPowerUp


class PowerUpFactory:
    def __init__(self, powerup_group):
        self.group = powerup_group
        self._last_kind = None
        self._streak = 0

    def create_random_powerup(self):
        x = SET.WIDTH + 40
        y = random.randint(50, SET.HEIGHT - 50)

        kind = random.choice(["shield", "shrink"])

        if kind == self._last_kind:
            self._streak += 1
            if self._streak >= 3:
                kind = "shrink" if kind == "shield" else "shield"
                self._last_kind = kind
                self._streak = 1
        else:
            self._last_kind = kind
            self._streak = 1

        if kind == "shield":
            pu = ShieldPowerUp(x, y)
        else:
            pu = ShrinkPowerUp(x, y)

        self.group.add(pu)
