import pygame, sys, time
from pygame.locals import QUIT
import random, math, json

# Start of fix
LEFT = -1
STILL = 0
RIGHT = 1
UP = -1
DOWN = 1
# End of fix

class Brain:
    def getAction(self, timestep: int, area: tuple, playerSize: tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockSize: tuple, blockPosition: tuple, blockVelocity: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        '''
        raise NotImplemented
    
class myBrain(Brain):
    def __init__(self):
        super().__init__()

    def getAction(self, timestep: int, area: tuple, playerSize: tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockSize: tuple, blockPosition: tuple, blockVelocity: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''
        choices = [-1, 0, 1]

        xDiff = myPosition[0] - enemyPosition[0]
        yDiff = myPosition[1] - enemyPosition[1]
        
        moveX: int = random.choice(choices)
        moveY: int = random.choice(choices)
        shootX: int = random.choice(choices)
        shootY: int = random.choice(choices)

        if xDiff > 0:
            shootX = -1
        else:
            shootX = 1
        if yDiff > 0:
            shootY = -1
        else:
            shootY = 1

        return ((moveX, moveY), (shootX, shootY))


class dumbBrain(Brain):
    def __init__(self):
        super().__init__()
    
    def getAction(self, timestep: int, area: tuple, playerSize: tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockSize: tuple, blockPosition: tuple, blockVelocity: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        x and y must each be either -1, 0, or 1.
        '''
        return ((0, 0), (0, 0))

class randomBrain(Brain):
    def __init__(self):
        super().__init__()

    def getAction(self, timestep: int, area: tuple, playerSize: tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockSize: tuple, blockPosition: tuple, blockVelocity: tuple) -> tuple:
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
    
    def getAction(self, timestep: int, area: tuple, playerSize: tuple, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockSize: tuple, blockPosition: tuple, blockVelocity: tuple) -> tuple:
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
        

def randomVelocity() -> tuple:
    choices = [-1, 0, 1]
    return (random.choice(choices), random.choice(choices))

def correctOutOfBounds(rect: pygame.Rect, bound: tuple) -> None:
    if rect.left < 0:
        rect.left = 0
    elif rect.right > bound[0]:
        rect.right = bound[0]
    if rect.top < 0:
        rect.top = 0
    elif rect.bottom > bound[1]:
        rect.bottom = bound[1]

def correctSATCollision(rect: pygame.Rect, block: pygame.Rect):
    # Separating Axis Theorem (SAT) collision detection implementation
    if rect.colliderect(block):
        overlap_x = rect.size[0]/2 + block.width/2 - abs(rect.centerx - block.centerx)
        overlap_y = rect.size[1]/2 + block.height/2 - abs(rect.centery - block.centery)

        if overlap_x < overlap_y:
            if rect.centerx < block.centerx:
                mtv = pygame.Vector2(-overlap_x, 0)
            else:
                mtv = pygame.Vector2(overlap_x, 0)
        else:
            if rect.centery < block.centery:
                mtv = pygame.Vector2(0, -overlap_y)
            else:
                mtv = pygame.Vector2(0, overlap_y)

        rect.move_ip(mtv)

class Bullet:
    def __init__(self, position: tuple, velocity: tuple, color: tuple):
        self.BORDERRADIUS = 5

        self._position: tuple = position
        self._velocity: tuple = velocity
        self._size: tuple = (5, 5)
        self._speed: int = 2
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        self._color = color

    @property
    def position(self) -> tuple:
        return self._position
    @property
    def velocity(self) -> tuple:
        return self._velocity
    @property
    def speed(self) -> int:
        return self._speed
    @property
    def size(self) -> tuple:
        return self._size
    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    @property
    def replayData(self) -> dict:
        return {
            "position": self._position,
            "velocity": self._velocity
        }
    
    def update(self):
        self._position = (self._position[0] + self._speed * self._velocity[0], self._position[1] + self._speed * self._velocity[1])
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self._rect, border_radius=self.BORDERRADIUS)

class Player:
    def __init__(self, brain: Brain, color: tuple, position: tuple = (0, 0), size: tuple = (30, 30), area: tuple = (500, 500)):
        self.BORDERRADIUS = 2
        
        self._size: tuple = size
        self._startPosition: tuple = position
        self._brain: Brain = brain
        self._bullets: list[Bullet] = []
        self._action: tuple = ((0, 0), (0, 0))
        self._speed: int = 1
        self._area: tuple = area
        self._rect: pygame.Rect = pygame.Rect(position[0], position[1], self._size[0], self._size[1])
        self._color: tuple = color

    @property
    def position(self) -> tuple:
        return (self._rect.x, self._rect.y)
    @property
    def velocity(self) -> tuple:
        return self._action[0]
    @property
    def color(self) -> tuple:
        return self._color
    @property
    def size(self) -> tuple:
        return self._size
    @property
    def bullets(self) -> list:
        return [(bullet.position, bullet.velocity) for bullet in self._bullets]
    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    @property
    def replayData(self) -> dict:
        return {
            "position": (self._rect.x, self._rect.y),
            "action": self._action,
            "bullets": [bullet.replayData for bullet in self._bullets]
        }

    @color.setter
    def color(self, color: tuple):
        self._color = color
    @size.setter
    def size(self, size: tuple):
        self._size = size

    def reset(self):
        self._rect = pygame.Rect(self._startPosition[0], self._startPosition[1], self._size[0], self._size[1])
        self._bullets = []
        self._action: tuple = ((0, 0), (0, 0))
    
    def shoot(self):
        if self._action[1] != (0, 0):
            self._shoot(self._action[1])

    def _shoot(self, direction: tuple):
        self._bullets.append(Bullet(self._rect.center, direction, self._color))

    def updateAction(self, timestep: int, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list, blockSize: tuple, blockPosition: tuple, blockVelocity: tuple):
        self._action = self._brain.getAction(timestep=timestep, area=self._area, playerSize=self._size,myPosition=(self._rect.x, self._rect.y), myVelocity=self._action[0], myBullets=self.bullets, enemyPosition=enemyPosition, enemyVelocity=enemyVelocity, enemyBullets=enemyBullets, blockSize=blockSize, blockPosition=blockPosition, blockVelocity=blockVelocity)
        assert(self._action[0][0] in [-1, 0, 1] and self._action[0][1] in [-1, 0, 1] and self._action[1][0] in [-1, 0, 1] and self._action[1][1] in [-1, 0, 1])

    def update(self, block: pygame.Rect, checkBlock: bool = True):
        self._rect.move_ip((self._action[0][0] * self._speed, self._action[0][1] * self._speed))
        
        if checkBlock:
            correctSATCollision(self._rect, block)
        correctOutOfBounds(self._rect, self._area)

        for bullet in self._bullets:
            bullet.update()
            # If bullet is out of bounds or touching the block, remove it
            if (checkBlock and bullet.rect.colliderect(block)) or bullet.position[0] < 0 or bullet.position[0] > self._area[0] or bullet.position[1] < 0 or bullet.position[1] > self._area[1]:
                self._bullets.remove(bullet)
    
    def _correctCollision(self, block: pygame.Rect):
        # Separating Axis Theorem (SAT) collision detection implementation
        if self._rect.colliderect(block):
            overlap_x = self._size[0]/2 + block.width/2 - abs(self._rect.centerx - block.centerx)
            overlap_y = self._size[1]/2 + block.height/2 - abs(self._rect.centery - block.centery)

            if overlap_x < overlap_y:
                if self._rect.centerx < block.centerx:
                    mtv = pygame.Vector2(-overlap_x, 0)
                else:
                    mtv = pygame.Vector2(overlap_x, 0)
            else:
                if self._rect.centery < block.centery:
                    mtv = pygame.Vector2(0, -overlap_y)
                else:
                    mtv = pygame.Vector2(0, overlap_y)

            self._rect.move_ip(mtv)

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self._rect, border_radius=self.BORDERRADIUS)

        for bullet in self._bullets:
            bullet.draw(surface)

class Game:
    def __init__(self, screen, area: tuple, bluePlayer: Player, redPlayer: Player, blockSize: tuple, blockMode: str = "random"):
        self.TELEUPDATEFREQUENCY: int = 200
        self.RANDOMUPDATEFREQUENCY: int = 100
        self.ACTIONUPDATEFREQUENCY: int = 10
        self.PLAYERSHOOTFREQUENCY: int = 20
        self.BACKGROUNDCOLOR = (200, 200, 200)
        self.BLOCKCOLOR = (30, 30, 30)
        self.BLOCKBORDERRADIUS = 2

        self._blockSize = blockSize
        self._screen = screen
        self._area: tuple = area
        self._bluePlayer: Player = bluePlayer
        self._redPlayer: Player = redPlayer
        self._players: list[Player] = [self._bluePlayer, self._redPlayer]
        assert blockMode in ["none", "tele", "path", "random"]
        self._blockMode: str = blockMode
        self._timestep: int = 0
        self._gameState: int = 0
        self._score: tuple = (0, 0)
        self._block: pygame.Rect = pygame.Rect(0, 0, self._blockSize[0], self._blockSize[1])
        self._blockVelocity = (0, 0)
        if blockMode == 'path':
            self._blockVelocity: tuple = (1, 0)
            self._blockSpeed: int = 1
            self._gapSize: int = 100
            self._block = pygame.Rect(self._gapSize, self._gapSize, self._blockSize[0], self._blockSize[1])
        elif blockMode == 'random':
            self._velocityChoices: list = [-1, 0 ,1]
            self._blockVelocity: tuple = randomVelocity()
            self._blockSpeed: int = 1
            self._block = self._createBlock()

    @property
    def timestep(self) -> int:
        return self._timestep
    @property
    def score(self) -> tuple:
        return self._score

    def reset(self):
        for player in self._players:
            player.reset()
        self._timestep = 0
        self._gameState = 0
        
        if self._blockMode == "tele":
            self._block = pygame.Rect(0, 0, self._blockSize[0], self._blockSize[1])
        elif self._blockMode == "path":
            self._block = pygame.Rect(self._gapSize, self._gapSize, self._blockSize[0], self._blockSize[1])
            self._blockVelocity = (1, 0)
        elif self._blockMode == "random":
            self._block = self._createBlock()
            self._blockVelocity = randomVelocity()
        
    def step(self):
        # Update player actions every 10 timesteps, allow players to shoot every 20 timesteps
        if self._timestep % self.ACTIONUPDATEFREQUENCY == 0:
            self.updateActions()
        if self._timestep % self.PLAYERSHOOTFREQUENCY == 0:
            for player in self._players:
                player.shoot()

        if self._blockMode != "none":
            self._updateBlock()

        # Update players (change position, etc.)
        for player in self._players:
            player.update(self._block, self._blockMode != "none")

        # Check if players have gotten shot
        self._checkShots()

        # Check player-player collisions
        self._checkCollisions()

        self._timestep += 1

        return self._gameState 

    def updateActions(self):
        self._bluePlayer.updateAction(self._timestep, self._redPlayer.position, self._redPlayer.velocity, self._redPlayer.bullets, self._blockSize, (self._block.x, self._block.y), self._blockVelocity)
        self._redPlayer.updateAction(self._timestep, self._bluePlayer.position, self._bluePlayer.velocity, self._bluePlayer.bullets, self._blockSize, (self._block.x, self._block.y), self._blockVelocity)

    def _checkShots(self):
        if self._bluePlayer.rect.collidelist(self._redPlayer.bullets) != -1:
            print("Blue player was shot!")
            self._gameState = 2
            self._score = (self._score[0], self._score[1] + 1)
        if self._redPlayer.rect.collidelist(self._bluePlayer.bullets) != -1:
            print("Red player was shot!")
            self._gameState = 1
            self._score = (self._score[0] + 1, self._score[1])

    def _checkCollisions(self):
        if self._bluePlayer.rect.colliderect(self._redPlayer.rect):
            print(f"Players collided!")
    
    def _updateBlock(self):
        if self._blockMode == "tele":
            self._updateTeleBlock()
        elif self._blockMode == "path":
            self._updatePathBlock()
        elif self._blockMode == "random":
            self._updateRandomBlock()

    def _updateTeleBlock(self):
        if self._timestep % self.TELEUPDATEFREQUENCY == 0:
            self._block = self._createBlock()
    
    def _updatePathBlock(self):
        self._block.move_ip((self._blockVelocity[0] * self._blockSpeed, self._blockVelocity[1] * self._blockSpeed))
        if self._block.right > self._area[0] - self._gapSize:
            self._block.right = self._area[0] - self._gapSize
            self._blockVelocity = (0, 1)
        elif self._block.left < self._gapSize:
            self._block.left = self._gapSize
            self._blockVelocity = (0, -1)
        elif self._block.top < self._gapSize:
            self._block.top = self._gapSize
            self._blockVelocity = (1, 0)
        elif self._block.bottom > self._area[1] - self._gapSize:
            self._block.bottom = self._area[1] - self._gapSize
            self._blockVelocity = (-1, 0)
    
    def _updateRandomBlock(self):
        if self._timestep % self.RANDOMUPDATEFREQUENCY == 0:
            self._blockVelocity = randomVelocity()

        self._block.move_ip((self._blockVelocity[0] * self._blockSpeed, self._blockVelocity[1] * self._blockSpeed))
        
        for player in self._players:
            correctSATCollision(self._block, player.rect)

        correctOutOfBounds(self._block, self._area)

        
    def _createBlock(self) -> pygame.Rect:
        block = pygame.Rect(random.randint(0, self._screen.get_width() - self._blockSize[0]), random.randint(0, self._screen.get_height() - self._blockSize[1]), self._blockSize[0], self._blockSize[1])
        while block.collidelist([player.rect for player in self._players]) != -1:
            block = pygame.Rect(random.randint(0, self._screen.get_width() - self._blockSize[0]), random.randint(0, self._screen.get_height() - self._blockSize[1]), self._blockSize[0], self._blockSize[1])
        return block

    def draw(self) -> str:
        self._screen.fill(self.BACKGROUNDCOLOR)

        # Draw the block
        if self._blockMode != "none":
            pygame.draw.rect(self._screen, self.BLOCKCOLOR, self._block, border_radius=self.BLOCKBORDERRADIUS)

        # Draw the players
        for player in self._players:
            player.draw(self._screen)
        
        pygame.display.flip()

        replayData = {
            "timestep": self._timestep,
            "bluePlayer": self._bluePlayer.replayData,
            "redPlayer": self._redPlayer.replayData,
            "block": {
                "position": (self._block.x, self._block.y),
                "velocity": self._blockVelocity
            }, 
            "score": self._score,
            "gameState": self._gameState
        }

        return json.dumps(replayData)


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

AREA = (600, 600)
PLAYERSIZE = (25, 25)
BLOCKSIZE = (80, 80)
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
