import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Action-Packed 2D Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5
        self.health = 100

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 4)

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Function to Generate Enemies
def generate_enemies(level):
    for _ in range(level * 5):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-150, -40)
        enemy = Enemy(x, y)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Function to Change Scenarios
def change_scenario(level):
    screen.fill(random.choice([BLACK, WHITE, (0, random.randint(0, 255), random.randint(0, 255))]))

# Sprite Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Player Instance
player = Player()
all_sprites.add(player)

# Main Game Loop
level = 1
score = 0

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Scenario Change
    change_scenario(level)

    # Level Progression
    if not enemies:
        level += 1
        generate_enemies(level)

    # Update
    all_sprites.update(keys)
    all_sprites.draw(screen)

    # Collision Detection
    for bullet in bullets:
        hit = pygame.sprite.spritecollideany(bullet, enemies)
        if hit:
            hit.kill()
            bullet.kill()
            score += 10

    # Player-Enemy Collision
    if pygame.sprite.spritecollideany(player, enemies):
        player.health -= 10
        if player.health <= 0:
            print(f"Game Over! Final Score: {score}")
            pygame.quit()
            sys.exit()

    # Draw HUD
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(level_text, (10, 70))

    pygame.display.flip()
    clock.tick(FPS)
