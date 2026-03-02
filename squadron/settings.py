import pygame
from enum import Enum, auto

pygame.init()

class Settings:
    #screen
    WIDTH = 1200
    HEIGHT = 800
    FPS = 60

    #speeds
    PLAYER_SPEED = 300
    PROJECTILE_SPEED_EASY = 250
    PROJECTILE_SPEED_HARD = 400

    #spawn intervals
    PROJECTILE_SPAWN_EASY = 1.2
    PROJECTILE_SPAWN_HARD = 0.7
    POWERUP_SPAWN_INTERVAL = 8.0

    #powerup duration
    SHIELD_DURATION = 4.0
    SHRINK_DURATION = 4.0
    SHRINK_FACTOR = 0.5

    #projectile sizes
    PROJECTILE_SIZES = [
        (40, 20),
        (70, 30)
    ]

    #colors
    COLOR_BG = (10, 10, 35)
    COLOR_TEXT = (230, 230, 230)
    COLOR_SHIELD = (80, 255, 150)

    #plane dimensions & gap size
    PLANE_WIDTH = 60
    PLANE_HEIGHT = 30
    PLANE_GAP_CLOSE = 40
    PLANE_GAP_MEDIUM = 90
    PLANE_GAP_WIDE = 150

    #difficulty
    class Difficulty(Enum):
        EASY = auto()
        HARD = auto()

    #formation
    class Formation(Enum):
        CLOSE = auto()
        MEDIUM = auto()
        WIDE = auto()

SET = Settings
