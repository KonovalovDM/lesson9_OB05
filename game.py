import pygame
import random

pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Пинг-понг")

clock = pygame.time.Clock()
fps = 60

# Звуковые эффекты
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")

# Шрифт для отображения текста
font = pygame.font.Font(None, 36)

class Rocket:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.radius = 8
        self.x = SCREEN_WIDTH // 2
        self.y = rocket.y - self.radius * 2
        self.speed_x = random.choice([-1, 1]) * 5
        self.speed_y = random.choice([-1, 1]) * 5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def check_collision(self):
        global hits, misses
        # Столкновение с ракеткой
        if self.y + self.radius >= rocket.y and rocket.x <= self.x <= rocket.x + rocket.width:
            self.speed_y = -self.speed_y
            pygame.mixer.Sound.play(hit_sound)
            hits += 1

        # Столкновение с краями экрана
        if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
            self.speed_x = -self.speed_x
            pygame.mixer.Sound.play(miss_sound)

        if self.y < self.radius:
            self.speed_y = -self.speed_y
            pygame.mixer.Sound.play(miss_sound)

        if self.y > SCREEN_HEIGHT:
            self.x = SCREEN_WIDTH // 2
            self.y = rocket.y - self.radius * 2
            self.speed_y = random.choice([-1, 1]) * 5
            pygame.mixer.Sound.play(miss_sound)
            misses += 1

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

class Game:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            rocket.move(keys)
            ball.move()
            ball.check_collision()

            rocket.draw()
            ball.draw()

            # Отображение счётчиков
            hits_text = font.render(f'Попадания: {hits}', True, (255, 255, 255))
            misses_text = font.render(f'Промахи: {misses}', True, (255, 255, 255))
            screen.blit(hits_text, (10, 10))
            screen.blit(misses_text, (10, 50))

            pygame.display.flip()
            clock.tick(fps)

            # Завершение игры при достижении 50 попаданий или промахов
            if hits >= 50 or misses >= 50:
                self.running = False


# Инициализация объектов
rocket = Rocket()
ball = Ball()
game = Game()

# Счетчик попаданий и промахов
hits = 0
misses = 0

game.run()
pygame.quit()
