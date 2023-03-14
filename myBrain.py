from game import Brain

class myBrain(Brain):
    def __init__(self):
        super().__init__()

    def getAction(self, myPosition: tuple, myVelocity: tuple,
                  enemyPosition: tuple, enemyVelocity: tuple,
                  closestBulletPosition: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''
        return ((0, 1), (1, 0))
