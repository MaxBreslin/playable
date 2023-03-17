from game import Brain
import random

class randomBrain(Brain):
    def __init__(self):
        super().__init__()

    def getAction(self, timestep: int, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''
        choices = [-1, 0, 1]

        moveX: int = random.choice(choices)
        moveY: int = random.choice(choices)
        shootX: int = random.choice(choices)
        shootY: int = random.choice(choices)

        return ((moveX, moveY), (shootX, shootY))