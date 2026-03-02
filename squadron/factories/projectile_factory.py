import random
from settings import SET
from entities.projectiles import Projectile

class ProjectileFactory:
    def __init__(self, difficulty_manager, projectile_group):
        self.diff = difficulty_manager
        self.group = projectile_group

    def create_random_projectile(self):
        w, h = random.choice(SET.PROJECTILE_SIZES)
        y = random.randint(40, SET.HEIGHT - 40)
        x = SET.WIDTH + w
        speed = self.diff.get_projectile_speed()
        proj = Projectile(x, y, w, h, speed)
        self.group.add(proj)
