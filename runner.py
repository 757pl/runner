import pygame
import random
pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Бесконечная дорога')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


player = pygame.Rect(100, 300, 50, 50)
jumping = False
jump_height = 10

score = 0
font = pygame.font.SysFont('Arial', 36)
clock = pygame.time.Clock()

obstacles = []
obstacle_speed = 5
obstacle_timer = 0


run = True
while run:
    screen.fill(WHITE)
    score_text = font.render('Очки:', score, True, (BLACK))
    screen.blit(score_text, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        jumping = True
    if jumping:
        player.y -= jump_height
        jump_height -= 0.5
        if jump_height < -10:
            jumping = False
            jump_height = 10
            player.y = 300
    obstacle_timer += 1
    if obstacle_timer > random.randint(50, 150):
        obstacles.append(pygame.Rect(800, 320, 30, 30))    
        obstacle_timer = 0

    for obstacle in obstacles[:]:
        obstacle.x -= obstacle_speed
        if obstacle.x < 30:
            obstacles.remove(obstacle)
            score += 1

    pygame.draw.rect(screen, (255, 0, 0), player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 0, 0), obstacle)


    clock.tick(60)
    pygame.display.update()
pygame.quit()