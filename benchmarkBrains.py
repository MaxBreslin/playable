from game import Brain, Bullet
import random, math

class dumbBrain(Brain):
    def __init__(self):
        super().__init__()
    
    def getAction(self, timestep: int, area:tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockPosition: tuple, blockVelocity: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''
        return ((0, 0), (0, 0))

class randomBrain(Brain):
    def __init__(self):
        super().__init__()

    def getAction(self, timestep: int, area:tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockPosition: tuple, blockVelocity: tuple) -> tuple:
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

class basicAimBrain(Brain):
    def __init__(self):
        super().__init__()
    
    def getAction(self, timestep: int, area:tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockPosition: tuple, blockVelocity: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''
        choices = [-1, 0, 1]

        if myPosition[0] > enemyPosition[0]:
            shootX = -1
        else:
            shootX = 1
        if myPosition[1] > enemyPosition[1]:
            shootY = -1
        else:
            shootY = 1
            
        moveX: int = random.choice(choices)
        moveY: int = random.choice(choices)
        
        return ((moveX, moveY), (shootX, shootY))

class basicAvoidBrain(Brain):
    def __init__(self):
        super().__init__()
    
    def getAction(self, timestep: int, area:tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockPosition: tuple, blockVelocity: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''

        if len(enemyBullets) == 0:
            return ((0, 0), (0, 0))

        moveX = 0
        moveY = 0
        closestBullet: Bullet = enemyBullets[0]

        distance = lambda x, y: math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
        closestDistance: float = distance(myPosition, closestBullet.position)
        
        for bullet in enemyBullets:
            if distance(myPosition, bullet.position) < closestDistance:
                closestDistance = distance(myPosition, bullet.position)
                closestBullet = bullet

        return ((moveX, moveY), (0, 0))
        
        