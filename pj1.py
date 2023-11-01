import pygame
from pygame.locals import *
from pygame import mixer
import math
import random
pygame.init()
screen = pygame.display.set_mode([800, 600])
bg = pygame.image.load('background.png')
player = pygame.image.load('player.png')
playerBoomimg = pygame.image.load('player_boom.png')
playerX = 380
playerY = 520
playerX_change = 2
playerY_change = 2
def fly (x, y):
    screen.blit(player, (x,y))
ufoImg = []
ufoX = []
ufoY = []
ufoX_change = []
ufoY_change = []
bulUfoX = []
bulUfoY = []
bulUfo_state = []
num_of_ufo = 6
UfoBoomIng = pygame.image.load('ufo_boom.png')
for i in range(num_of_ufo):
    ufoImg.appeng(pygame.image.load('ufo.png'))
    ufoX.append(random.randint(0, 740))
    ufoY.append(random.randint(0, 250))
    ufoX_change.append(random.randint(-1, 1))
    ufoY_change.append(1)
    bulUfoX.append(0)
    bulUfoY.append(0)
    bulUfo_state.append("standby")
def ufo (x, y, i):
    screen.blit(ufoImg[i], (x, y))
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 0
bulletY_change = 15
bullet_state = "standby"
def fire(x, y):
    global bullet_state
    bullet_state = "shoot"
    screen.blit(bulletImg, (x+16 , y-16))
bulUfoY_change = 2
def ufo_fire(x, y):
    global bulUfo_state
    bulUfo_state[i] = "shoot"
    screen.blit(bulletImg, (x+16 , y+16))
def collisionBulletPlayer_UFO(ufoX, ufoY, bulletX, bulletY):
    distance = math.sqrt((math.pow(ufoX-bulletX, 2)) + (math.pow(ufoY-bulletY, 2)))
    if distance < 40:
        return True
    else :
        return False
def collisionBulletUFO_player(x1, y1, x2, y2):
    distace = math.sqrt((math.pow(x1-x2, 2)) + (math.pow(y1-y2,2)))
    if distace < 40:
        return True
    else:
        return False
def UfoClashplayer(x1, y1, x2, y2):
    distace = math.sqrt(math.pow(x1-x2, 2)) + (math.pow(y1-y2,2))
    if distace < 40 :
        return True
    else:
        return False
def PlayerBoom(x, y):
    screen.blit(playerBoomimg, (x, y))
    pygame.display.update()
    pygame.time.delay(50)
score = 0
font0bj = pygame.font.Font('freesansbold.ttf', 30)
scoreX = 15
scoreY = 15
def show_score(x, y):
    scoreText = font0bj.render('Score: '+ str(score),True,'WHITE')
    screen.blit(scoreText, (x, y))
bgSound = mixer.Sound('bg.wav')
endState = "standby"
def gameOver():
    global endState
    endState = "end"
def showEnd():
    font0bj = pygame.font.Font('freesansbold.ttf', 60)
endText = font0bj.render('Game Over', True,'WHITE')
screen.blit(endText, (220, 230)) 
global PlayerY
PlayerY = -100
bgSound = mixer.Sound('bg.wav')
bgSound.play(-1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running =False
    screen.blit(bg, (0, 0))
    key = pygame.key.get_pressed()
    if key[K_UP]: playerY -= playerY_change
    if key[K_DOWN]: playerY += playerY_change
    if key[K_LEFT]: playerX -= playerX_change
    if key[K_RIGHT]: playerX += playerX_change
    if endState == "standby":
        if playerX < 0: playerX = 0
        if playerX >740: playerX = 740
        if playerY <= 0: playerY = 0
        if playerY >=540: playerY =540
    fly(playerX, playerY)
    if key[K_SPACE]:
        if bullet_state == "standby" and endState == "standby":
            shootSound = mixer.Sound('shoot.wav')
            shootSound.play()
            bulletX = playerX
            bulletY = playerY
            fire(bulletX, bulletY)
        if bullet_state == "shoot":
            bulletY -= bulletY_change
            fire(bulletX,bulletY)
    if bulletY <= 0:
        bullet_state ="standby"
    for i in range(num_of_ufo):
        ufoX[i] += ufoX_change[i]
        ufoY[i] += ufoY_change[i]
        if ufoX[i] <=0:
            ufoX_change[i] = 1
        if ufoX[i] >740:
            ufoX_change[i] = -1
        if ufoY[i] >=600:
            ufoY[i] = 0
            ufoX[i] = random.randint(0, 740)
        ufo(ufoX[i], ufoY[i], i)
    if bulUfo_state[i] == "standby":
        shootUfoSound = mixer.Sound('ufo_fire.wav')
        shootSound.play()
        bulletX[i] = ufoX[i]
        bulletY[i] = ufoY[i]
        ufo_fire(bulUfoX[i], bulUfoY[i])
    if bulUfo_state[i] == "shoot":
        bulUfoY[i] += bulUfoY_change
        ufo_fire(bulUfoX[i], bulUfoY[i])
    if bulUfoY[i] >= 600:
        bulUfoY[i] = ufoY[i]
        bulUfo_state[i] = "standby"
    collision = collisionBulletPlayer_UFO(ufoX[i], ufoY[i], bulletX, bulletY)
        
    if collision:
        bullet_state = "standby"
        score +=10
        ufoExplosion = mixer.Sound('explosion.wav')
        ufoExplosion.play()
        UfoBoom(ufoX[i], ufoY[i])
        ufoY[i] = 700
        bulletY = -200
    collisionPlayer = collisionBulletPlayer_UFO(playerX, playerY, bulUfoX[i], bulUfoY[i])
    if collisionPlayer:
        PlayerExplision = mixer.Sound('explosion.mp3')
        PlayerExplision.play()
        PlayerBoom(playerX, playerY)
        gameOver()
    ClashPlayer = UfoClashplayer(ufoX[i], ufoY[i], playerX,playerY)
    if ClashPlayer:
        clashUfo = mixer.Sound('explosion.mp3')
        clashUfo.play()
        PlayerBoom(playerX, playerY)
        gameOver()
if endState == "end":
    showEnd()
show_score(scoreX, scoreY)
pygame.display.update()