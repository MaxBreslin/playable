import pygame
from pygame.locals import QUIT
from game import Player, Brain, Game
from benchmarkBrains import *

pygame.init()

AREA = (500, 500)
PLAYERSIZE = (30, 30)
DISPLAYSURF = pygame.display.set_mode(AREA)
pygame.display.set_caption("")

clock = pygame.time.Clock()
FRAMERATE = 60

redBrain: Brain = randomBrain()
redPlayer: Player = Player(redBrain, (180, 60, 60), (0, 0), PLAYERSIZE, AREA)
blueBrain: Brain = randomBrain()
bluePlayer: Player = Player(blueBrain, (60, 60, 180), (AREA[0] - PLAYERSIZE[0], AREA[1] - PLAYERSIZE[1]), PLAYERSIZE, AREA)

blockMode = "random"

game = Game(DISPLAYSURF, AREA, bluePlayer, redPlayer, blockMode)

running = True

while running:
    gamestate = game.step()
    game.draw()

    if gamestate != 0:
        print(f"Score: {game.score}")
        game.reset()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    clock.tick(FRAMERATE)

pygame.quit()
