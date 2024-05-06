# main.py

import pygame
import sys
import time
import settings
import sprites
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FRAMERATE
from sprites import BG, Ground, Plane, Obstacle


print(dir(settings))
print(dir(sprites))

class Game:
    def __init__(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird 2.0')
        self.clock = pygame.time.Clock()
        self.active = True
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Calculate scale factor based on background image
        try:
            bg_img = pygame.image.load("assets/background.jpg")
            bg_height = bg_img.get_height()
            self.scale_factor = WINDOW_HEIGHT / bg_height
        except Exception as e:
            print(f"Error loading background image: {e}")
            pygame.quit()
            sys.exit()

        # Set up sprites
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
        self.plane.rect.center = (100, WINDOW_HEIGHT / 2)

        # Set up obstacle timer event (generates obstacles periodically)
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Load font for displaying score
        try:
            self.font = pygame.font.Font("assets/BD_Cartoon_Shout.ttf", 30)
        except Exception as e:
            print(f"Error loading font: {e}")
            pygame.quit()
            sys.exit()

        self.score = 0
        self.start_offset = 0

        # Set up menu for when the game is paused
        try:
            self.menu_surf = pygame.image.load("assets/menu.png").convert_alpha()
            self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        except Exception as e:
            print(f"Error loading menu image: {e}")
            pygame.quit()
            sys.exit()

        # Play background music in a loop
        try:
            self.music = pygame.mixer.Sound("assets/bg_sound.wav")
            self.music.set_volume(0.3)  # Adjust volume as needed
            self.music.play(loops=-1)
        except Exception as e:
            print(f"Error loading music: {e}")
            pygame.quit()
            sys.exit()

    def check_collisions(self):
        # Check if the plane hits an obstacle or the top of the screen
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            # Remove obstacles and deactivate the game if collision occurs
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        # Calculate score based on time elapsed
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            score_y_pos = WINDOW_HEIGHT / 10
        else:
            score_y_pos = WINDOW_HEIGHT / 2 + self.menu_rect.height / 1.5

        # Render and display score on screen
        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, score_y_pos))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        # Main game loop
        last_time = time.time()
        while True:
            # Calculate delta time
            dt = time.time() - last_time
            last_time = time.time()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        # Jump the plane if active
                        self.plane.jump()
                    else:
                        # Restart the game if inactive
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                # Handle obstacle creation on a timer
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            # Update the game state
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            # Check for collisions or display the menu if the game is paused
            if self.active:
                self.check_collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            # Refresh the display
            pygame.display.update()

            # Limit the frame rate for smoother gameplay
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    # Start the game
    game = Game()
    game.run()
