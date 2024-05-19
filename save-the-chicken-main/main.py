import pygame
import random
import math
from pygame import mixer
#farmer,foxes,balls,bgm,background screen,score,ball sound,splash sound

#initialization
pygame.init()

#createscreen
screen=pygame.display.set_mode((800,600))

#backgroundimage
background=pygame.image.load('newbackgnew.jpg')

#BGM
mixer.music.load('farm_music.wav.mp3')
mixer.music.play(-1)

#name&logo
pygame.display.set_caption("Save the chicken!!!")
icon=pygame.image.load('chickennewnext.png')
pygame.display.set_icon(icon)

#spaceship
farmerImg=pygame.image.load('farmer_with_water_balloon_new.png')
farmerX = 370
farmerY = 480
farmerX_change = 0

#enemies multiply
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    # enemy
    enemyImg.append(pygame.image.load('foxnew.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(10)

#bullet
bulletImg=pygame.image.load('waterballonnew.png')
bulletX=50
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

#score
score_value = 0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#game over
over_font=pygame.font.Font('freesansbold.ttf',100)

# collision
def ifCollision(enemyX,enemyY,bulletX,bulletY):
    Distance = math.dist((enemyX,enemyY),(bulletX,bulletY))
    if Distance<32:
        return True
    else:
        return False

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(100,250))

def farmer(x,y):
    screen.blit(farmerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#gameloop
running=True
while running:
    #RGB
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                farmerX_change=-5
            if event.key==pygame.K_RIGHT:
                farmerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletsound=mixer.Sound("throw.wav")
                    bulletsound.play()
                    bulletX=farmerX
                    fire_bullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                farmerX_change=0
    farmerX+=farmerX_change

    #setboundaries for player
    if farmerX<=0:
        farmerX=0
    if farmerX>=736:
        farmerX=736

    for i in range(num_of_enemies):
        if enemyY[i] > 450:
                for j in range(num_of_enemies):
                    enemyY[j]=1000
                game_over_text()
                break

    #setboundaries for enemy
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=1
            enemyY[i]+=enemyY_change[i]
        if enemyX[i]>=736:
            enemyX_change[i]=-1
            enemyY[i]+=enemyY_change[i]

    # collision impact
        collision = ifCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
            bulletY=480
            score_value+=1
            explosionsound=mixer.Sound("water.wav")
            explosionsound.play()
            bullet_state="ready"
        enemy(enemyX[i], enemyY[i], i)

    #setboundaries for bullet
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    farmer(farmerX,farmerY)
    show_score(textX,textY)
    pygame.display.update()