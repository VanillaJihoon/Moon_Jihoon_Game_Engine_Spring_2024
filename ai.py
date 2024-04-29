import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player attributes
PLAYER_SIZE = 30
PLAYER_SPEED = 5

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Screen with Player")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Create the player
player = Player()

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main loop
running = True
player_dx = 0
player_dy = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_dx = PLAYER_SPEED
            elif event.key == pygame.K_UP:
                player_dy = -PLAYER_SPEED
            elif event.key == pygame.K_DOWN:
                player_dy = PLAYER_SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_dy = 0

    # Move the player
    player.update(player_dx, player_dy)

    # Adjust the screen position based on player's position
    screen_x = player.rect.centerx - SCREEN_WIDTH // 2
    screen_y = player.rect.centery - SCREEN_HEIGHT // 2

    # Render sprites at adjusted positions
    screen.fill(WHITE)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - screen_x, sprite.rect.y - screen_y))
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()