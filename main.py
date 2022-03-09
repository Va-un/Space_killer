import math  # importing important files
import pygame
import random
from pygame import mixer

# start the pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))  # width  x height                                                         #creating a tab of specific size

# adding title and icon
pygame.display.set_caption("Space invaders")  # giving heading to tab
icon = pygame.image.load('icons8-viper-mark-2-48.png')  # giving image to tab
pygame.display.set_icon(icon)

# background

background = pygame.image.load('space.png')  # adding a background image remember image should as size of tab created
mixer.music.load('background.wav')
mixer.music.play(-1)  # it will play only once so to keep it in loop we write -1

# player set up
playerImg = pygame.image.load('fighter.png')
playerX = 370  # setting up co-ordinates so that player appears in middle
playerY = 480
playerX_change = 0

# score
font = pygame.font.Font('freesansbold.ttf', 32)  # font + size
textX = 10
textY = 10
score_value = 0


# game over function
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):  # show  score
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


# setting enemy number in array so that we don't have to write code again and again
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):  # saving the values
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# setting bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready - means cant see bullet on screen  fire - can see bullet on screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))



def isclollision(enemyX, enemyY, bulletX, bulletY):  # collision checker checks if bullet has collided
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 26:  # since distance from center to end of the image is 27 approx
        return True
    else:
        return False


#  game loop makes sure the  game is running , any thing you want consistent should be kept here
running = True
while running:  # main loop in which will keep the game running until done
    screen.fill((0, 0, 0))  # R  G B if u want a colour background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if closed the closes
            running = False

        if event.type == pygame.KEYDOWN:  # checks if key is pressed or not

            if event.key == pygame.K_LEFT:  # moves left
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # moves right
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()  # as we want to play it only once
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # sees if uve stop pressing the key
            playerX_change = 0  # it will add null does making the player stop moving

    playerX += playerX_change  # final  change is added before screen refreshes

    # detection system next 4 lines it makes it such as you cannot leave the boundaries of the  plane
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # checking boundaries for enemy + its movement + adding game over in it
    for i in range(num_of_enemies):  # runs a loop so that each and every enemy behaves like this
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_over = mixer.Sound('game_over.wav')
            game_over.play(1)  # as we want to play it only once

            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # for collision if collided or not
        collision = isclollision(enemyX[i], enemyY[i], bulletX, bulletY)  # stores value  true or false
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()  # as we want to play it only once
            bulletX = playerX
            bulletY = 480  # resetting the bullet to starting point
            bullet_state = "fire"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)  # refreshes enemy everytime killed

    # bullet movement mech
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()  # update the display
