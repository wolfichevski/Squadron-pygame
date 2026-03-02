import pygame


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.rect.x -= int(150 * dt)
        if self.rect.right < 0:
            self.kill()

    def apply(self, game):
        raise NotImplementedError()


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        img = pygame.image.load("assets/shield.png").convert_alpha()
        img = pygame.transform.smoothscale(img, (25, 25))
        super().__init__(x, y, img)

    def apply(self, game):
        game.activate_shield()


class ShrinkPowerUp(PowerUp):
    def __init__(self, x, y):
        img = pygame.image.load("assets/shrink.png").convert_alpha()
        img = pygame.transform.smoothscale(img, (25, 25))
        super().__init__(x, y, img)

    def apply(self, game):
        game.activate_shrink()
