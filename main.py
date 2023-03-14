import pygame, sys
from pygame.locals import QUIT
from game import Player

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
DISPLAYSURF.fill((255, 255, 255))

player: Player = Player()

while True:
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), pygame.Rect(player.size[0], player.size[1], player.size[0], player.size[1]))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()