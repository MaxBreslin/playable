import pygame
from pygame.locals import QUIT
from game import Player, Brain
from myBrain import myBrain

pygame.init()

AREA = (400, 400)
DISPLAYSURF = pygame.display.set_mode(AREA)
background_color = (255, 255, 255)
DISPLAYSURF.fill(background_color)

clock = pygame.time.Clock()
frameRate = 30
frameCount = 0

brain1: Brain = myBrain()
player1: Player = Player(brain1, (0, 0), AREA)
brain2: Brain = Brain()
player2: Player = Player(brain2, (200, 200), AREA)

running = True

inRange = lambda x, y, r: (x[0] <= y[0] <= x[0]+r[0]) and (x[1] <= y[1] <= x[1]+r[1])

while running:
    for bullet in player1.bullets:
        if inRange(player2.position, bullet.position, player2.size):
            print("Player 2 shot!")
            running = False
    for bullet in player2.bullets:
        if inRange(player1.position, bullet.position, player1.size):
            print("Player 1 shot!")
            running = False
      
  
    player1.update()
    player2.update()
    if frameCount >= 10:
        player1.updateAction(player2.position, player2.velocity, (0, 0))
        player2.updateAction(player1.position, player1.velocity, (0, 0))
        frameCount = 0

    player1.draw(DISPLAYSURF)
    player2.draw(DISPLAYSURF)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    pygame.display.flip()
    DISPLAYSURF.fill(background_color)

    frameCount += 1
    clock.tick(frameRate)

pygame.quit()
