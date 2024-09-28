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

# Параметры ракетки
rocket_width, rocket_height = 100, 10
rocket_x = SCREEN_WIDTH // 2 - rocket_width // 2
rocket_y = SCREEN_HEIGHT - rocket_height
rocket_speed = 5

# Параметры мяча
ball_radius = 8
ball_x = SCREEN_WIDTH // 2
ball_y = rocket_y - ball_radius * 2
ball_speed_x = random.choice([-1, 1]) * 5  # Скорость мяча
ball_speed_y = random.choice([-1, 1]) * 5

# Цвет фона
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Звуковые эффекты
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")

# Счетчик попаданий и промахов
hits = 0
misses = 0

# Шрифт для отображения текста
font = pygame.font.Font(None, 36)

# Основной цикл игры до 50 промахов или принудительного выхода
running = True
while running:
    screen.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение ракетки
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_x > 0:
        rocket_x -= rocket_speed
    if keys[pygame.K_RIGHT] and rocket_x < SCREEN_WIDTH - rocket_width:
        rocket_x += rocket_speed

        # Движение мяча
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Проверка столкновения мяча и ракетки
    if ball_y + ball_radius >= rocket_y and rocket_x <= ball_x <= rocket_x + rocket_width:
        ball_speed_y = -ball_speed_y
        pygame.mixer.Sound.play(hit_sound)
        hits += 1

    # Проверка столкновения с краями экрана
    if ball_x < ball_radius or ball_x > SCREEN_WIDTH - ball_radius:
        ball_speed_x = -ball_speed_x
        pygame.mixer.Sound.play(miss_sound)

    if ball_y < ball_radius:
        ball_speed_y = -ball_speed_y
        pygame.mixer.Sound.play(miss_sound)

    if ball_y > SCREEN_HEIGHT:
        ball_x = SCREEN_WIDTH // 2
        ball_y = rocket_y - ball_radius * 2
        ball_speed_y = random.choice([-1, 1]) * 5
        pygame.mixer.Sound.play(miss_sound)
        misses += 1

    # Отображение ракетки и мяча
    pygame.draw.rect(screen, (255, 255, 255), (rocket_x, rocket_y, rocket_width, rocket_height))
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)

    # Отображение счётчиков
    hits_text = font.render(f'Попадания: {hits}', True, (255, 255, 255))
    misses_text = font.render(f'Промахи: {misses}', True, (255, 255, 255))
    screen.blit(hits_text, (10, 10))
    screen.blit(misses_text, (10, 50))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()