import pygame, sys, time
from pygame.locals import QUIT
from game import Player, Brain, Game
from benchmarkBrains import *
from myBrain import myBrain

def getBrainObject(brainName: str) -> Brain:
    for moduleName, module in list(sys.modules.items()):
        try:
            brain = getattr(module, brainName)
            if not issubclass(type(brain), type(Brain)):
                pass
            return brain()
        except AttributeError:
            pass
    else:
        raise ValueError(f"Could not find class {blueBrainName}")

pygame.init()

AREA = (300, 300)
PLAYERSIZE = (20, 20)
BLOCKSIZE = (50, 50)
FRAMERATE = 60

blueBrainName: str = input("Enter blue brain (e.g. randomBrain, myBrain): ")
if blueBrainName == "":
    blueBrainName = "myBrain"

blueBrain = getBrainObject(blueBrainName)

bluePlayer: Player = Player(blueBrain, (60, 60, 180), (AREA[0] - PLAYERSIZE[0], AREA[1] - PLAYERSIZE[1]), PLAYERSIZE, AREA)

redBrainName: str = input("Enter red brain: ")
if redBrainName == "":
    redBrainName = "randomBrain"

redBrain = getBrainObject(redBrainName)

redPlayer: Player = Player(redBrain, (180, 60, 60), (0, 0), PLAYERSIZE, AREA)

blockMode: str = input("Enter block mode (e.g. random, none): ")
if blockMode == "":
    blockMode = "random"

DISPLAYSURF = pygame.display.set_mode(AREA)
pygame.display.set_caption("")
clock = pygame.time.Clock()

game = Game(DISPLAYSURF, AREA, bluePlayer, redPlayer, BLOCKSIZE, blockMode)

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
