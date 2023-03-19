import pygame, sys, random

class Brain:
    def getAction(self, timestep: int, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        '''
        raise NotImplemented

class Bullet:
    def __init__(self, position: tuple, velocity: tuple, color: tuple):
        self.BORDERRADIUS = 3

        self._position: tuple = position
        self._velocity: tuple = velocity
        self._size: tuple = (5, 5)
        self._speed: float = 1.5
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        self._color = color

    @property
    def position(self) -> tuple:
        return self._position
    @property
    def velocity(self) -> tuple:
        return self._velocity
    @property
    def size(self) -> tuple:
        return self._size
    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    def update(self):
        self._position = (self._position[0] + self._speed * self._velocity[0], self._position[1] + self._speed * self._velocity[1])
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self._rect, border_radius=self.BORDERRADIUS)

class Player:
    def __init__(self, brain: Brain, name: str, bulletColor: tuple, position: tuple = (0, 0), area: tuple = (500, 500)):
        self.BORDERRADIUS = 2

        self._size: tuple = (30, 30)
        self._startPosition: tuple = position
        self._name: str = name
        self._brain: Brain = brain
        self._bullets: list = []
        self._action: tuple = ((0, 0), (0, 0))
        self._speed: float = 1
        self._area: tuple = area
        self._nameSurface = pygame.font.SysFont('calibri', 30).render(name, True, (255, 255, 255))
        self._rect: pygame.Rect = pygame.Rect(position[0], position[1], self._size[0], self._size[1])
        self._bulletColor = bulletColor

    @property
    def position(self) -> tuple:
        return (self._rect.x, self._rect.y)
    @property
    def velocity(self) -> tuple:
        return self._action[0]
    @property
    def name(self) -> str:
        return self._name
    @property
    def size(self) -> tuple:
        return self._size
    @property
    def bullets(self) -> list:
        return self._bullets
    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @name.setter
    def name(self, name: str):
        self._name = name
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
        self._bullets.append(Bullet(self._rect.center, direction, self._bulletColor))

    def updateAction(self, timestep: int, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list):
        self._action = self._brain.getAction(timestep, (self._rect.x, self._rect.y), self._action[0], self._bullets, enemyPosition, enemyVelocity, enemyBullets)
        assert(self._action[0][0] in [-1, 0, 1] and self._action[0][1] in [-1, 0, 1] and self._action[1][0] in [-1, 0, 1] and self._action[1][1] in [-1, 0, 1])

    def update(self, blocks: list):
        self._rect.move_ip((self._action[0][0] * self._speed, self._action[0][1] * self._speed))
        
        for block in blocks:
            self._correctCollision(block)
        self._correctOutOfBounds()

        for bullet in self._bullets:
            bullet.update()
            # If bullet is out of bounds or touching the block, remove it
            if bullet.rect.colliderect(blocks[0]) or bullet.position[0] < 0 or bullet.position[0] > self._area[0] or bullet.position[1] < 0 or bullet.position[1] > self._area[1]:
                self._bullets.remove(bullet)
    
    def _correctOutOfBounds(self):
        if self._rect.left < 0:
            self._rect.left = 0
        elif self._rect.right > self._area[0]:
            self._rect.right = self._area[0]
        if self._rect.top < 0:
            self._rect.top = 0
        elif self._rect.bottom > self._area[1]:
            self._rect.bottom = self._area[1]
    
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
        pygame.draw.rect(surface, (0, 0, 0), self._rect, border_radius=self.BORDERRADIUS)
        surface.blit(self._nameSurface, self._rect)

        for bullet in self._bullets:
            bullet.draw(surface)

class Game:
    def __init__(self, screen, player1: Player, player2: Player, blockSize: tuple = (80, 80)):
        self.BLOCKUPDATEFREQUENCY: int = 200
        self.ACTIONUPDATEFREQUENCY: int = 10
        self.PLAYERSHOOTFREQUENCY: int = 20
        self.BACKGROUNDCOLOR = (200, 200, 200)
        self.BLOCKCOLOR = (30, 30, 30)
        self.NEXTBLOCKCOLOR = (180, 180, 180)
        self.BLOCKBORDERRADIUS = 2

        self._blockSize = blockSize
        self._player1: Player = player1
        self._player2: Player = player2
        self._players: list = [self._player1, self._player2]
        self._screen = screen
        self._timestep: int = 0
        self._gameState: int = 0
        self._score: tuple = (0, 0)
        self._block: pygame.Rect = pygame.Rect(0, 0, self._blockSize[0], self._blockSize[1])
        self._nextBlock: pygame.Rect = self._createBlock()

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
        self._block = pygame.Rect(0, 0, self._blockSize[0], self._blockSize[1])
        self._nextBlock = self._createBlock()
        
    def step(self):
        # Update player actions every 10 timesteps, allow players to shoot every 20 timesteps
        if self._timestep % self.ACTIONUPDATEFREQUENCY == 0:
            self.updateActions()
        if self._timestep % self.PLAYERSHOOTFREQUENCY == 0:
            for player in self._players:
                player.shoot()
        if self._timestep % self.BLOCKUPDATEFREQUENCY == 0:
            self._updateBlock()

        # Update players (change position, etc.)
        for player in self._players:
            player.update([self._block, self._nextBlock])

        self._checkShots()
        self._checkCollisions()
        self._timestep += 1

        return self._gameState

    def updateActions(self):
        self._player1.updateAction(self._timestep, self._player2.position, self._player2.velocity, self._player2.bullets)
        self._player2.updateAction(self._timestep, self._player1.position, self._player1.velocity, self._player1.bullets)

    def _checkShots(self):
        if self._player1.rect.collidelist(self._player2.bullets) != -1:
            print(f"{self._player1.name} was shot!")
            self._gameState = 2
            self._score = (self._score[0], self._score[1] + 1)
        if self._player2.rect.collidelist(self._player1.bullets) != -1:
            print(f"{self._player2.name} was shot!")
            self._gameState = 1
            self._score = (self._score[0] + 1, self._score[1])

    def _checkCollisions(self):
        if self._player1.rect.colliderect(self._player2.rect):
            print(f"Players collided!")
    
    def _updateBlock(self):
        self._block = self._nextBlock
        self._nextBlock = self._createBlock()
    
    def _createBlock(self) -> pygame.Rect:
        block = pygame.Rect(random.randint(0, self._screen.get_width() - self._blockSize[0]), random.randint(0, self._screen.get_height() - self._blockSize[1]), self._blockSize[0], self._blockSize[1])
        while block.collidelist([player.rect for player in self._players]) != -1 or block.colliderect(self._block):
            block = pygame.Rect(random.randint(0, self._screen.get_width() - self._blockSize[0]), random.randint(0, self._screen.get_height() - self._blockSize[1]), self._blockSize[0], self._blockSize[1])
        return block

    def draw(self):
        self._screen.fill(self.BACKGROUNDCOLOR)

        # Draw the block
        pygame.draw.rect(self._screen, self.BLOCKCOLOR, self._block, border_radius=self.BLOCKBORDERRADIUS)

        # Draw the next block
        pygame.draw.rect(self._screen, self.NEXTBLOCKCOLOR, self._nextBlock, border_radius=self.BLOCKBORDERRADIUS)
        timeTillNextBlock = int((self.BLOCKUPDATEFREQUENCY - (self._timestep % self.BLOCKUPDATEFREQUENCY)) / self.BLOCKUPDATEFREQUENCY * 20) + 1
        timer = pygame.font.SysFont('calibri', 30).render(str(timeTillNextBlock), True, (255, 255, 255))
        self._screen.blit(timer, self._nextBlock)

        # Draw the players
        for player in self._players:
            player.draw(self._screen)
        
        pygame.display.flip()
