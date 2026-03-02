import pygame
from settings import SET


class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_width = SET.PLANE_WIDTH
        self.base_height = SET.PLANE_HEIGHT

        self.image = pygame.image.load("assets/plane.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.base_width, self.base_height))
        self.rect = self.image.get_rect(center=(x, y))

    def set_pos(self, x, y):
        self.rect.center = (x, y)


class Squadron:
    def __init__(self, center_x, center_y, formation_manager):
        self.formation_manager = formation_manager
        self.center_x = center_x
        self.center_y = center_y
        self.planes = [
            Plane(center_x, center_y),
            Plane(center_x, center_y),
        ]
        self.update_positions()

    def update_positions(self):
        gap = self.formation_manager.get_gap()
        self.planes[0].set_pos(self.center_x, self.center_y - gap / 2)
        self.planes[1].set_pos(self.center_x, self.center_y + gap / 2)

    def move_vertical(self, dy_per_sec, dt):
        self.center_y += dy_per_sec * dt

        min_y = min(p.rect.top for p in self.planes)
        max_y = max(p.rect.bottom for p in self.planes)

        if min_y < 0:
            self.center_y -= min_y
        elif max_y > SET.HEIGHT:
            self.center_y -= (max_y - SET.HEIGHT)

        self.update_positions()

    def set_formation_changed(self):
        self.update_positions()

    def draw(self, surf, shield_active: bool):
        for p in self.planes:
            surf.blit(p.image, p.rect)
            if shield_active:
                pygame.draw.rect(surf, SET.COLOR_SHIELD, p.rect.inflate(8, 8), 2)
