import pygame, sys
from pygame.locals import QUIT
from game import Player, Brain, Game
from myBrain import myBrain

pygame.init()

AREA = (500, 500)
DISPLAYSURF = pygame.display.set_mode(AREA)
background_color = (255, 255, 255)
DISPLAYSURF.fill(background_color)

clock = pygame.time.Clock()
frameRate = 30
frameCount = 0

brain: Brain = myBrain()
player1: Player = Player(brain)
player2: Player = Player(brain, (100, 100))

running = True

while running:

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
sys.exit()
