import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1435
SCREEN_HEIGHT = 783

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Dot Game with Enemies")

# Dot properties
dot_size = 10
dot_x = SCREEN_WIDTH // 2
dot_y = SCREEN_HEIGHT // 2
dot_color = WHITE
dot_speed = 5

# Enemy properties
enemy_size = 20
enemy_speed = 2

# Projectile properties
projectile_width = 5
projectile_height = 10
projectile_speed = 6

# Initial spawn rates
initial_enemy_spawn_rate = 2000  # milliseconds
initial_projectile_spawn_rate = 500  # milliseconds, faster than before

# Game properties
game_over = False
score = 0
lives = 3

# Multipliers for increasing difficulty
spawn_multiplier = 2
projectile_multiplier = 3
score_milestone = 100

# Current rates
current_enemy_spawn_rate = initial_enemy_spawn_rate
current_projectile_spawn_rate = initial_projectile_spawn_rate

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 20  # Frames per second

# Lists to hold enemies, projectiles, and explosions
enemies = []
projectiles = []
explosions = []

# Font for displaying the score and lives
font = pygame.font.Font(None, 36)

# Function to change the dot color randomly
def change_dot_color():
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color != RED and color != GREEN and color != BLACK:
            return color

# Function to spawn a new enemy
def spawn_enemy():
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)
    enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_size)
    enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))

# Function to spawn a new projectile from a random enemy
def spawn_projectile():
    if enemies:
        enemy = random.choice(enemies)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # 8 directions
        direction = random.choice(directions)
        projectile_x = enemy.x + enemy_size // 2
        projectile_y = enemy.y + enemy_size // 2
        projectiles.append({
            'rect': pygame.Rect(projectile_x, projectile_y, projectile_width, projectile_height),
            'direction': direction
        })

# Function to reset the game
def reset_game():
    global dot_x, dot_y, dot_color, game_over, enemies, projectiles, score, lives, explosions, current_enemy_spawn_rate, current_projectile_spawn_rate
    dot_x = SCREEN_WIDTH // 2
    dot_y = SCREEN_HEIGHT // 2
    dot_color = WHITE
    game_over = False
    enemies = []
    projectiles = []
    score = 0
    lives = 3
    explosions = []
    current_enemy_spawn_rate = initial_enemy_spawn_rate
    current_projectile_spawn_rate = initial_projectile_spawn_rate
    pygame.time.set_timer(pygame.USEREVENT + 1, current_enemy_spawn_rate)
    pygame.time.set_timer(pygame.USEREVENT + 2, current_projectile_spawn_rate)

# Class for explosion animation
class Explosion:
    def __init__(self, x, y):
        self.frames = [pygame.Surface((40, 40), pygame.SRCALPHA) for _ in range(10)]
        for frame in self.frames:
            frame.fill((0, 0, 0, 0))
            pygame.draw.circle(frame, (255, 69, 0), (20, 20), 20)
            pygame.draw.circle(frame, (255, 140, 0), (20, 20), 15)
            pygame.draw.circle(frame, (255, 215, 0), (20, 20), 10)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0
    
    def update(self):
        self.timer += 1
        if self.timer % 3 == 0:
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                return False  # Animation is complete
        return True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Timers for enemy and projectile spawning
pygame.time.set_timer(pygame.USEREVENT + 1, initial_enemy_spawn_rate)
pygame.time.set_timer(pygame.USEREVENT + 2, initial_projectile_spawn_rate)
pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  # 1 second timer for score increment

# Function to draw the start screen
def draw_start_screen():
    screen.fill(BLACK)
    # Draw the start button
    button_width, button_height = 200, 50
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT - button_height - 50
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
    start_text = font.render("Click to Start", True, BLACK)
    screen.blit(start_text, (button_x + (button_width - start_text.get_width()) // 2, button_y + (button_height - start_text.get_height()) // 2))
    pygame.display.flip()

# Main game loop
running = True
show_start_screen = True

while running:
    if show_start_screen:
        draw_start_screen()
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_click = False
        show_start_screen = False
        reset_game()
    
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_start_screen = True
        elif event.type == pygame.USEREVENT + 1:
            spawn_enemy()
        elif event.type == pygame.USEREVENT + 2:
            spawn_projectile()
        elif event.type == pygame.USEREVENT + 3:
            score += 1
            if score % score_milestone == 0:
                current_enemy_spawn_rate = max(500, int(current_enemy_spawn_rate / spawn_multiplier))
                current_projectile_spawn_rate = max(100, int(current_projectile_spawn_rate / projectile_multiplier))
                pygame.time.set_timer(pygame.USEREVENT + 1, current_enemy_spawn_rate)
                pygame.time.set_timer(pygame.USEREVENT + 2, current_projectile_spawn_rate)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        dot_x -= dot_speed
    if keys[pygame.K_d]:
        dot_x += dot_speed
    if keys[pygame.K_w]:
        dot_y -= dot_speed
    if keys[pygame.K_s]:
        dot_y += dot_speed
    if keys[pygame.K_e]:
            dot_color = change_dot_color()

    
    if dot_x < 0 or dot_x > SCREEN_WIDTH - dot_size:
        dot_color = change_dot_color()
        dot_x = max(0, min(dot_x, SCREEN_WIDTH - dot_size))
    if dot_y < 0 or dot_y > SCREEN_HEIGHT - dot_size:
        dot_color = change_dot_color()
        dot_y = max(0, min(dot_y, SCREEN_HEIGHT - dot_size))

    dot_rect = pygame.Rect(dot_x, dot_y, dot_size, dot_size)
    pygame.draw.rect(screen, dot_color, dot_rect)

    for projectile in projectiles[:]:
        direction_x, direction_y = projectile['direction']
        projectile['rect'].x += direction_x * projectile_speed
        projectile['rect'].y += direction_y * projectile_speed

        if projectile['rect'].colliderect(dot_rect):
            lives -= 1
            projectiles.remove(projectile)
            explosions.append(Explosion(dot_x, dot_y))
            if lives == 0:
                game_over = True
                break
        elif (projectile['rect'].x < 0 or projectile['rect'].x > SCREEN_WIDTH or
              projectile['rect'].y < 0 or projectile['rect'].y > SCREEN_HEIGHT):
            projectiles.remove(projectile)
        else:
            pygame.draw.rect(screen, GREEN, projectile['rect'])
    
    for explosion in explosions[:]:
        if not explosion.update():
            explosions.remove(explosion)
        else:
            explosion.draw(screen)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

    pygame.display.flip()

    if game_over:
        pygame.time.wait(2000)
        reset_game()
        show_start_screen = True

    clock.tick(FPS)

pygame.quit()
