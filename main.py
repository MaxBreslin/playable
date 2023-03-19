import pygame
from pygame.locals import QUIT
from game import Player, Brain, Game
from benchmarkBrains import *

pygame.init()

AREA = (500, 500)
DISPLAYSURF = pygame.display.set_mode(AREA)
pygame.display.set_caption("")

clock = pygame.time.Clock()
FRAMERATE = 60

redBrain: Brain = randomBrain()
redPlayer: Player = Player(redBrain, (180, 60, 60), (0, 0), AREA)
blueBrain: Brain = randomBrain()
bluePlayer: Player = Player(blueBrain, (60, 60, 180), (200, 200), AREA)

game = Game(DISPLAYSURF, bluePlayer, redPlayer)

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
