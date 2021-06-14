import pygame
from pygame import mixer
import random
import math
import time

# Initialization of pygame
pygame.init()

# Creating screen
screen = pygame.display.set_mode((800, 600))

# Title & Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('background.png')

# BackGround Music
fireSound = mixer.Sound('gunFire.ogg')
hitSound = mixer.Sound('gunHit.ogg')

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 536

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(30, 150))
    enemyX_change.append(0.1*random.randint(2,3))
    enemyY_change.append(random.randint(20,40))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 300
bulletY = 400
bulletX_change = 0
bulletY_change = 1.4
bullet_state = 'ready' # ready- you can't see the bullet on screen
                       # fire - Bullet moving

# Score
score = 0
font = pygame.font.Font('FiraCode-Bold.ttf', 42)
textX, textY = 570, 10

# Game Over
gameOverFont = pygame.font.Font('Poppins-Bold.ttf', 72)

# Velocity of Spaceship
global velocityX
global velocityY

velocityX, velocityY = 0, 0

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollide(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow((bulletX - enemyX), 2) + math.pow((bulletY - enemyY), 2))
    if dist < 28:
        return True
    else:
        return False

def get_score(x, y):
    Score = font.render(f'Score: {score}', True, (248, 236, 67))
    screen.blit(Score, (x, y))

def gameOver():
    Game_Over = gameOverFont.render('GAME OVER', True, (51, 153, 245))
    screen.blit(Game_Over, (200, 200))
    

# Game Loop
running = True
while running:

    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keys are pressed
        if event.type == pygame.KEYDOWN:
            # Left Right Movement
            if event.key == pygame.K_LEFT:
                # playerX -= velocity
                velocityX = -0.5
            if event.key == pygame.K_RIGHT:
                # playerX += velocity
                velocityX = 0.5
            
            # Up Down movement
            if event.key == pygame.K_UP:
                # playerY -= velocity
                velocityY = -0.5
            if event.key == pygame.K_DOWN:
                # playerY += velocity
                velocityY = 0.5

            # bullet firing 
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    bulletY = playerY
                    fireSound.play()
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            # Left Right Movement
            if event.key == pygame.K_LEFT:
                # playerX -= velocity
                velocityX = 0
            if event.key == pygame.K_RIGHT:
                # playerX += velocity
                velocityX = 0
            
            # Up Down movement
            if event.key == pygame.K_UP:
                # playerY -= velocity
                velocityY = 0
            if event.key == pygame.K_DOWN:
                # playerY += velocity
                velocityY = 0

    playerX += velocityX
    playerY += velocityY


    # Creating Boundary for player
    if playerX <= 0:
        playerX = 0
    
    if playerX >= 736:
        playerX = 736
    
    if playerY <= 500:
        playerY = 500
    
    if playerY >= 536:
        playerY = 536
    
    # enemyY_change = random.randint(20,40)
    

    # Creating Boundary for enemy
    for i in range(no_of_enemies):

        # Game Over
        if enemyY[i] > 550:
            for j in range(no_of_enemies):
                enemyY[j] = -500
            gameOver()
            time.sleep(5)
            pygame.quit()

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.1*random.randint(2,3)
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.1*random.randint(2,3)
            enemyY[i] += enemyY_change[i]

        if isCollide(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = playerY
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(30, 150)
            hitSound.play()
            score += 1
        
        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement
    if bulletY <= -30:
        bulletY = playerY
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    get_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()



pygame.quit()
