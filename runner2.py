import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 250
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Динозаврик")
clock = pygame.time.Clock()

dino_img = pygame.image.load("dino.png")
dino_duck_img = pygame.image.load("dino_duck.png")
cactus_img = pygame.image.load("cactus.png")
bird_img = pygame.image.load("bird.png")

dino_rect = pygame.Rect(50, GROUND_HEIGHT - 50, 30, 50)
dino_velocity_y = 0
dino_jumping = False
dino_ducking = False

obstacles = []
obstacle_timer = 0
obstacle_frequency = 1500

score = 0
game_speed = 5
game_over = False

font = pygame.font.SysFont('Arial', 36)

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    
    # Рестарт игры
    if game_over:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                game_over = False
                score = 0
                game_speed = 5
                obstacles = []
                dino_rect.y = GROUND_HEIGHT - 50
                dino_velocity_y = 0
                dino_jumping = False
                dino_ducking = False
        continue  # Пропускаем остальную обработку, если игра окончена
    
    # Прыжок
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
            if dino_jumping == False and dino_ducking == False:
                dino_velocity_y = -15
                dino_jumping = True
    
    # Приседание
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            if dino_jumping == False:
                dino_ducking = True
                dino_rect.height = 30
                dino_rect.y = GROUND_HEIGHT - 30
    
    # Вставание
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            if dino_ducking == True:
                dino_ducking = False
                dino_rect.height = 50
                dino_rect.y = GROUND_HEIGHT - 50
    
    if not game_over:
        # Гравитация для динозаврика
        dino_velocity_y += 0.8
        dino_rect.y += dino_velocity_y
        
        # Проверка на землю
        if dino_rect.bottom > GROUND_HEIGHT:
            dino_rect.bottom = GROUND_HEIGHT
            dino_velocity_y = 0
            dino_jumping = False
        
        # Генерация препятствий
        obstacle_timer += clock.get_time()
        if obstacle_timer > obstacle_frequency:
            obstacle_timer = 0
            obstacle_type = random.choice(["cactus", "bird"])
            
            if obstacle_type == "cactus":
                obstacle_rect = pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - 50, 20, 50)
            else:  # bird
                obstacle_rect = pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - random.randint(70, 120), 40, 20)
            
            obstacles.append({"rect": obstacle_rect, "type": obstacle_type})
        
        # Обновление препятствий
        for obstacle in obstacles[:]:
            obstacle["rect"].x -= game_speed
            
            # Проверка столкновений
            if dino_rect.colliderect(obstacle["rect"]):
                game_over = True
            
            # Удаление препятствий за экраном
            if obstacle["rect"].right < 0:
                obstacles.remove(obstacle)
        
        # Увеличение счета и скорости
        score += 1
        if score % 500 == 0:
            game_speed += 0.5
            obstacle_frequency = max(500, obstacle_frequency - 50)
    
    # Отрисовка
    screen.fill(WHITE)
    
    # Линия земли
    pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)
    
    # Отрисовка динозаврика
    if dino_ducking:
        screen.blit(dino_duck_img, dino_rect)
    else:
        screen.blit(dino_img, dino_rect)
    
    # Отрисовка препятствий
    for obstacle in obstacles:
        if obstacle["type"] == "cactus":
            screen.blit(cactus_img, obstacle["rect"])
        else:
            screen.blit(bird_img, obstacle["rect"])
    
    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Сообщение о конце игры
    if game_over:
        game_over_text = font.render("Игра окончена! Нажмите SPACE для рестарта", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 18))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()