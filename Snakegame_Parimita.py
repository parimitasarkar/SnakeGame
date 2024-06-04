import pygame
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Snake:
    def __init__(self, difficulty):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)  # Start moving up
        self.food = self.generate_food()
        self.score = 0
        self.speed = 5 * difficulty  # Adjust speed based on difficulty

    def move(self):
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        if head in self.snake[:-1] or not (0 <= head[0] < GRID_WIDTH) or not (0 <= head[1] < GRID_HEIGHT):
            return False
        self.snake.insert(0, head)
        if head == self.food:
            self.food = self.generate_food()
            self.score += 1
        else:
            self.snake.pop()
        return True

    def change_direction(self, direction):
        if direction == 'UP' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == 'DOWN' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif direction == 'LEFT' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == 'RIGHT' and self.direction != (-1, 0):
            self.direction = (1, 0)

    def generate_food(self):
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        while food in self.snake:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        return food

    def draw(self, surface):
        for segment in self.snake:
            pygame.draw.rect(surface, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Scoreboard:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0

    def update(self, score):
        self.score = score

    def draw(self, surface):
        text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(text, (10, 10))

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    start_font = pygame.font.Font(None, 36)
    start_text = start_font.render("Click to Start", True, WHITE)
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Click to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    scoreboard = Scoreboard()
    difficulty = int(input("Choose difficulty (1 - Easy, 2 - Medium, 3 - Hard): "))
    snake = Snake(difficulty)
    game_over = False
    running = False  # Game not started yet
    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = True

        window.fill(BLACK)
        if not game_over:
            window.blit(start_text, start_rect)
        else:
            window.blit(restart_text, restart_rect)
        pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                snake = Snake(difficulty)
                game_over = False

        window.fill(BLACK)
        if not snake.move():
            game_over = True  # Game over if snake cannot move
            game_over_text = scoreboard.font.render("Game Over!", True, RED)
            window.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20))
        snake.draw(window)
        scoreboard.update(snake.score)
        scoreboard.draw(window)
        pygame.display.update()
        clock.tick(snake.speed)

    pygame.quit()

if __name__ == "__main__":
    main()
