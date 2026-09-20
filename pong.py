import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game objects dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 6

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Bug fix: was placing top-left at center
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = 5 * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom with position correction
        if self.rect.top <= 0:
            self.speed_y = abs(self.speed_y)   # Bug fix: clamp direction + correct position
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -abs(self.speed_y)  # Bug fix: clamp direction + correct position
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = 5 * random.choice([-1, 1])


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)

        self.left_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()

        self.left_score = 0
        self.right_score = 0

    def handle_collisions(self):
        # Ball collision with paddles
        if self.ball.rect.colliderect(self.left_paddle.rect):
            if self.ball.speed_x < 0:
                self.ball.speed_x *= -1
                self.ball.rect.left = self.left_paddle.rect.right

        if self.ball.rect.colliderect(self.right_paddle.rect):
            if self.ball.speed_x > 0:
                self.ball.speed_x *= -1
                self.ball.rect.right = self.right_paddle.rect.left

        # Ball out of bounds (scoring)
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()

        if self.ball.rect.right >= SCREEN_WIDTH:
            self.left_score += 1
            self.ball.reset()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Left paddle controls (W and S)
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        # Right paddle controls (UP and DOWN arrows)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()

    def update(self):
        self.ball.update()
        self.handle_collisions()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw paddles and ball
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 15):
            pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH // 2, y), (SCREEN_WIDTH // 2, y + 10), 2)

        # Draw scores
        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (SCREEN_WIDTH // 4, 50))
        self.screen.blit(right_text, (3 * SCREEN_WIDTH // 4, 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.update()
            self.draw()

            self.clock.tick(60)  # 60 FPS

        pygame.quit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
