import random
import pgzrun
import pygame
from pgzero.animation import animate
from pgzero.builtins import Actor
from pgzero.keyboard import keyboard
from pgzero.loaders import sounds
from pgzero.screen import Screen
from pygame import time

screen: Screen

WIDTH = 800
HEIGHT = 600
TITLE = "CHASE GAME"
background = Actor("space")
player = Actor("alien")
player.x = 500
player.y = 450

enemy_right = Actor("monster_1")
enemy_left = Actor('monster_1_left')
enemy = Actor("monster_1")
coin = Actor("cristal_2", pos=(300, 300))
score = 0
time2 = 20
loose = 0
win=0

def draw():
    screen.clear()
    background.draw()
    coin.draw()
    player.draw()
    enemy.draw()
    score_string = str(score)
    screen.draw.text(f"Punkty:{score_string}", (0, 0), color='green')
    time2_string = str(round(time2))
    screen.draw.text(f"Czas:{time2_string}", (150, 0), color='green')
    if score >= 5 and loose == 0:
        screen.draw.text(f"Wygrales!!!!", (HEIGHT // 2, 200),
                         fontsize=60, owidth=1.5, ocolor=(255, 255, 0), color=(0, 0, 0))
        sounds.eep.stop()

    if loose == 1:
        screen.draw.text(f"Ups!Przegrales", (HEIGHT // 2, 200),
                         fontsize=60, owidth=1.5, ocolor=(255, 255, 0), color=(0, 0, 0))

    # animate(enemy_left,tween='bounce_start',pos=(100, 300),duration=200)


def update(delta):
    global score, time2, loose, enemy,win
    time2 = time2 - delta

    if time2 <= 0:
        loose = 1
    if keyboard.right:
        player.x = player.x + 4
    if keyboard.left:
        player.x = player.x - 4
    if keyboard.down:
        player.y = player.y + 4
    if keyboard.up:
        player.y = player.y - 4

    if player.right > WIDTH:
        player.right = WIDTH
    if player.left < 0:
        player.left = 0
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    if enemy.x < player.x:
        print(enemy.x, player.x)
        enemy_right.x = enemy.x
        enemy_right.y = enemy.y
        enemy = enemy_right
    enemy.x = enemy.x + 0.5
    if enemy.x > player.x:
        enemy_left.x = enemy.x
        enemy_left.y = enemy.y
        enemy = enemy_left
        enemy.x = enemy.x - 1
    if enemy.y < player.y:
        enemy.y = enemy.y + 1

    if enemy.y > player.y:
        enemy.y = enemy.y - 1

    def set_alien_normal():
        player.image = 'alien'

    if player.colliderect(enemy):
        if loose != 1:
            player.image = 'alien_hurt'
            loose = 1
            clock.schedule_unique(set_alien_normal, 1.0)
            # player.image = 'alien'
            sounds.eep.play()

    if keyboard.d:
        player.x = player.x + 4
    if keyboard.a:
        player.x = player.x - 4
    if keyboard.s:
        player.y = player.y + 4
    if keyboard.w:
        player.y = player.y - 4
    # coin swings
    coin.angle += 1
    if coin.colliderect(player):
        sounds.blop.play()
        coin.x = random.randint(0, WIDTH - 20)
        coin.y = random.randint(0, HEIGHT - 20)
        score = score + 1
        print("Score:", score)


# images = ["alien_hurt", "alien"]
# image_counter = 0
#
# def animateAlien():
#     global image_counter
#     player.image = images[image_counter % len(images)]
#     image_counter += 1
#
#     clock.schedule_interval(animateAlien, 0.2)

images1 = ["monster_1", "monster_1_left"]
image_counter1 = 0


def animateEnemy() -> object:
    global image_counter1
    enemy.image = images1[image_counter1 % len(images1)]
    image_counter1 += 1


clock.schedule_interval(animateEnemy, 0.5)

pgzrun.go()
