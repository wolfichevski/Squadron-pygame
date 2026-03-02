import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed):
        super().__init__()
        self.base_size = (w, h)
        self.current_scale = 1.0
        self.speed = speed

        self.image = pygame.image.load("assets/projectile.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.smoothscale(self.image, self.base_size)

        self.rect = self.image.get_rect(midright=(x, y))

    def apply_shrink(self, factor: float):
        self.current_scale = factor
        w = max(4, int(self.base_size[0] * factor))
        h = max(4, int(self.base_size[1] * factor))

        center = self.rect.center

        self.image = pygame.image.load("assets/projectile.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.smoothscale(self.image, (w, h))
        self.rect = self.image.get_rect(center=center)

    def update(self, dt: float):
        self.rect.x -= int(self.speed * dt)
        if self.rect.right < 0:
            self.kill()
