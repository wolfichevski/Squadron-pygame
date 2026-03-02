from settings import SET

class DifficultyManager:
    def __init__(self):
        self.current = SET.Difficulty.EASY

    def toggle(self):
        self.current = (
            SET.Difficulty.HARD
            if self.current == SET.Difficulty.EASY
            else SET.Difficulty.EASY
        )

    def get_projectile_speed(self):
        return (SET.PROJECTILE_SPEED_EASY
                if self.current == SET.Difficulty.EASY
                else SET.PROJECTILE_SPEED_HARD)

    def get_spawn_interval(self):
        return (SET.PROJECTILE_SPAWN_EASY
                if self.current == SET.Difficulty.EASY
                else SET.PROJECTILE_SPAWN_HARD)
