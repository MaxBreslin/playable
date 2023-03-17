import pygame
from pygame.locals import QUIT
from game import Player, Brain, Game
from benchmarkBrains import randomBrain

pygame.init()

AREA = (500, 500)
DISPLAYSURF = pygame.display.set_mode(AREA)
background_color = (255, 255, 255)
DISPLAYSURF.fill(background_color)

clock = pygame.time.Clock()
FRAMERATE = 60

brain1: Brain = randomBrain()
player1: Player = Player(brain1, "Player 1", (255, 0, 0), (0, 0), AREA)
brain2: Brain = randomBrain()
player2: Player = Player(brain2, "Player 2", (0, 0, 255), (200, 200), AREA)

game = Game(DISPLAYSURF, player1, player2)

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
