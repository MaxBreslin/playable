import pygame, sys
from pygame.locals import QUIT
from game import Player, Brain, Game
from myBrain import myBrain

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
DISPLAYSURF.fill((255, 255, 255))

clock = pygame.time.Clock()
frameRate = 1

brain: Brain = myBrain()
player1: Player = Player(brain)
player2: Player = Player(brain, (100, 100))


while True:

    player1.update(player2.position, player2.velocity, (0, 0))
    player2.update(player1.position, player1.velocity, (0, 0))
    player1.draw(DISPLAYSURF)
    player2.draw(DISPLAYSURF)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()

    clock.tick(frameRate)