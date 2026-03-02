import os
import random
import pygame

from settings import SET
from managers.difficulty_manager import DifficultyManager
from managers.formation_manager import FormationManager
from entities.planes import Squadron
from factories.projectile_factory import ProjectileFactory
from factories.powerup_factory import PowerUpFactory

HIGH_SCORE_FILE = "highscore.txt"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SET.WIDTH, SET.HEIGHT))
        pygame.display.set_caption("Squadron")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)

        self.running = True
        self.in_menu = True
        self.game_over = False

        self.selected_difficulty = SET.Difficulty.EASY

        self.difficulty_manager = DifficultyManager()
        self.formation_manager = FormationManager()

        self.squadron = Squadron(
            SET.PLANE_WIDTH + 20,
            SET.HEIGHT / 2,
            self.formation_manager,
        )

        self.projectiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.projectile_factory = ProjectileFactory(self.difficulty_manager, self.projectiles)
        self.powerup_factory = PowerUpFactory(self.powerups)

        self.time_since_last_projectile = 0.0
        self.time_since_last_powerup = 0.0
        self.next_powerup_spawn_interval = self._roll_next_powerup_interval()

        self.shield_active = False
        self.shield_timer = 0.0

        self.shrink_active = False
        self.shrink_timer = 0.0
        self.global_shrink_factor = 1.0

        self.distance = 0.0
        self.best_distance = self.load_best_distance()

    # -------- high score --------

    def load_best_distance(self) -> float:
        if not os.path.exists(HIGH_SCORE_FILE):
            return 0.0
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
                txt = f.read().strip()
            return float(txt) if txt else 0.0
        except Exception:
            return 0.0

    def save_best_distance(self) -> None:
        try:
            with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
                f.write(str(self.best_distance))
        except Exception:
            pass

    # -------- powerups --------

    def _roll_next_powerup_interval(self) -> float:
        base = SET.POWERUP_SPAWN_INTERVAL
        return base + random.uniform(base * 0.75, base * 1.75)

    def activate_shield(self) -> None:
        self.shield_active = True
        self.shield_timer = SET.SHIELD_DURATION

    def activate_shrink(self) -> None:
        self.shrink_active = True
        self.shrink_timer = SET.SHRINK_DURATION
        self.global_shrink_factor = SET.SHRINK_FACTOR
        for p in self.projectiles:
            p.apply_shrink(self.global_shrink_factor)

    def update_powerups_state(self, dt: float) -> None:
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.shrink_active:
            self.shrink_timer -= dt
            if self.shrink_timer <= 0:
                self.shrink_active = False
                self.global_shrink_factor = 1.0
                for p in self.projectiles:
                    p.apply_shrink(1.0)

    # -------- state resets --------

    def _reset_run_state(self) -> None:
        self.distance = 0.0
        self.projectiles.empty()
        self.powerups.empty()

        self.time_since_last_projectile = 0.0
        self.time_since_last_powerup = 0.0
        self.next_powerup_spawn_interval = self._roll_next_powerup_interval()

        self.shield_active = False
        self.shield_timer = 0.0

        self.shrink_active = False
        self.shrink_timer = 0.0
        self.global_shrink_factor = 1.0

        self.formation_manager.current = SET.Formation.MEDIUM
        self.squadron.set_formation_changed()

    def start_game_from_menu(self) -> None:
        self.difficulty_manager.current = self.selected_difficulty
        self._reset_run_state()
        self.game_over = False
        self.in_menu = False

    def reset_after_game_over(self) -> None:
        self._reset_run_state()
        self.game_over = False
        self.in_menu = True

    # -------- main loop --------

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(SET.FPS) / 1000.0
            self.handle_events()
            if not self.in_menu and not self.game_over:
                self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.running = False
                continue

            if self.in_menu:
                if event.key == pygame.K_1:
                    self.selected_difficulty = SET.Difficulty.EASY
                elif event.key == pygame.K_2:
                    self.selected_difficulty = SET.Difficulty.HARD
                elif event.key == pygame.K_RETURN:
                    self.start_game_from_menu()
                continue

            if self.game_over:
                if event.key == pygame.K_SPACE:
                    self.reset_after_game_over()
                continue

            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                self.formation_manager.set_by_number(event.key - pygame.K_0)
                self.squadron.set_formation_changed()
            elif event.key == pygame.K_f:
                self.formation_manager.cycle()
                self.squadron.set_formation_changed()

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.squadron.move_vertical(-SET.PLAYER_SPEED, dt)
        elif keys[pygame.K_s]:
            self.squadron.move_vertical(SET.PLAYER_SPEED, dt)

        speed_factor = 1.0 if self.difficulty_manager.current == SET.Difficulty.EASY else 1.3
        self.distance += 150 * speed_factor * dt
        if self.distance > self.best_distance:
            self.best_distance = self.distance

        self.time_since_last_projectile += dt
        if self.time_since_last_projectile >= self.difficulty_manager.get_spawn_interval():
            self.time_since_last_projectile = 0.0

            count = 1 if self.difficulty_manager.current == SET.Difficulty.EASY else random.randint(1, 3)
            before = set(self.projectiles.sprites())

            for _ in range(count):
                self.projectile_factory.create_random_projectile()

            if self.global_shrink_factor != 1.0:
                for p in self.projectiles:
                    if p not in before:
                        p.apply_shrink(self.global_shrink_factor)

        self.time_since_last_powerup += dt
        if self.time_since_last_powerup >= self.next_powerup_spawn_interval:
            self.time_since_last_powerup = 0.0
            self.next_powerup_spawn_interval = self._roll_next_powerup_interval()
            self.powerup_factory.create_random_powerup()

        self.projectiles.update(dt)
        self.powerups.update(dt)
        self.update_powerups_state(dt)

        for plane in self.squadron.planes:
            for pu in pygame.sprite.spritecollide(plane, self.powerups, dokill=True):
                pu.apply(self)

        if self.shield_active:
            return

        for plane in self.squadron.planes:
            if pygame.sprite.spritecollide(plane, self.projectiles, dokill=False):
                self.game_over = True
                self.save_best_distance()
                return

    # -------- drawing --------

    def draw_text(self, text: str, x: float, y: float, *, align_right=False, color=None) -> None:
        if color is None:
            color = SET.COLOR_TEXT
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(topleft=(x, y))
        if align_right:
            rect.topright = (x, y)
        self.screen.blit(surf, rect)

    def draw_menu(self) -> None:
        text_col = SET.COLOR_TEXT

        title = self.font.render("SQUADRON – SETUP", True, text_col)
        self.screen.blit(title, title.get_rect(center=(SET.WIDTH / 2, 80)))

        color_easy = (0, 255, 0) if self.selected_difficulty == SET.Difficulty.EASY else text_col
        color_hard = (0, 255, 0) if self.selected_difficulty == SET.Difficulty.HARD else text_col

        self.draw_text("[1] EASY", SET.WIDTH / 2 - 80, 150, color=color_easy)
        self.draw_text("[2] HARD", SET.WIDTH / 2 - 80, 180, color=color_hard)
        self.draw_text("ENTER to start", SET.WIDTH / 2 - 90, 240)
        self.draw_text("In-game: [1/2/3] formations, [F] cycle formations", SET.WIDTH / 2 - 350, 300)
        self.draw_text(f"Best distance: {int(self.best_distance)}", SET.WIDTH / 2 - 120, 360)

    def draw(self) -> None:
        self.screen.fill(SET.COLOR_BG)

        if self.in_menu:
            self.draw_menu()
            pygame.display.flip()
            return

        self.squadron.draw(self.screen, self.shield_active)

        self.projectiles.draw(self.screen)
        self.powerups.draw(self.screen)

        self.draw_text(f"Distance: {int(self.distance)}", 10, 10)
        self.draw_text(f"Best: {int(self.best_distance)}", 10, 40)

        diff_str = "EASY" if self.difficulty_manager.current == SET.Difficulty.EASY else "HARD"
        form_str = {
            SET.Formation.CLOSE: "CLOSE",
            SET.Formation.MEDIUM: "MEDIUM",
            SET.Formation.WIDE: "WIDE",
        }[self.formation_manager.current]
        self.draw_text(f"Difficulty: {diff_str} | Formation: {form_str}", 10, 70)

        if self.shield_active:
            self.draw_text(f"Shield: {self.shield_timer:0.1f}s", SET.WIDTH - 10, 10, align_right=True)
        if self.shrink_active:
            self.draw_text(f"Shrink: {self.shrink_timer:0.1f}s", SET.WIDTH - 10, 40, align_right=True)

        if self.game_over:
            text_col = SET.COLOR_TEXT
            msg = self.font.render(f"GAME OVER – Distance: {int(self.distance)}", True, text_col)
            msg2 = self.font.render("Press SPACE to go to menu", True, text_col)
            self.screen.blit(msg, msg.get_rect(center=(SET.WIDTH / 2, SET.HEIGHT / 2 - 20)))
            self.screen.blit(msg2, msg2.get_rect(center=(SET.WIDTH / 2, SET.HEIGHT / 2 + 20)))

        pygame.display.flip()
