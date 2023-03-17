import pygame, sys

class Brain:
    def getAction(self, timestep: int, myPosition: tuple, myVelocity: tuple, myBullets: list, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        '''
        raise NotImplemented

class Bullet:
    def __init__(self, position: tuple, velocity: tuple, color: tuple):
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
        pygame.draw.rect(surface, self._color, self._rect)

class Player:
    def __init__(self, brain: Brain, name: str, bulletColor: tuple, position: tuple = (0, 0), area: tuple = (500, 500)):
        self._position: tuple = position
        self._startPosition: tuple = position
        self._velocity: tuple = (0, 0)
        self._name: str = name
        self._size: tuple = (30, 30)
        self._brain: Brain = brain
        self._bullets: list = []
        self._action: tuple = ((0, 0), (0, 0))
        self._speed: float = 0.75
        self._area: tuple = area
        self._nameSurface = pygame.font.SysFont('Arial', 8).render(name, True, (255, 255, 255))
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        self._bulletColor = bulletColor

    @property
    def position(self) -> tuple:
        return self._position
    @property
    def velocity(self) -> tuple:
        return self._velocity
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
        self._position = self._startPosition
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        self._velocity = (0, 0)
        self._bullets = []
        self._action: tuple = ((0, 0), (0, 0))
    
    def shoot(self):
        if self._action[1] != (0, 0):
            self._shoot(self._action[1])

    def _shoot(self, direction: tuple):
        self._bullets.append(Bullet((self._position[0]+self._size[0]//2, self._position[1]+self._size[1]//2), direction, self._bulletColor))

    def updateAction(self, timestep: int, enemyPosition: tuple, enemyVelocity: tuple, enemyBullets: list):
        self._action = self._brain.getAction(timestep, self._position, self._velocity, self._bullets, enemyPosition, enemyVelocity, enemyBullets)
        assert(self._action[0][0] in [-1, 0, 1] and self._action[0][1] in [-1, 0, 1] and self._action[1][0] in [-1, 0, 1] and self._action[1][1] in [-1, 0, 1])
        self._velocity = self._action[0]

    def update(self):
        clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        self._position = (clamp(self._position[0] + self._speed * self._velocity[0], 0, self._area[0] - self._size[0]), clamp(self._position[1] + self._speed * self._velocity[1], 0, self._area[1] - self._size[1]))
        self._rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        for bullet in self._bullets:
            bullet.update()
            if bullet.position[0] < 0 or bullet.position[0] > self._area[0] or bullet.position[1] < 0 or bullet.position[1] > self._area[1]:
                self._bullets.remove(bullet)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self._rect)
        surface.blit(self._nameSurface, self._rect)

        for bullet in self._bullets:
            bullet.draw(surface)

class Game:
    def __init__(self, screen, player1, player2):
        self._player1: Player = player1
        self._player2: Player = player2
        self._players: list = [self._player1, self._player2]
        self._screen = screen
        self._timestep: int = 0
        self._gameState = 0
        self._score = (0, 0)

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
        
    def step(self):
        if self._timestep % 10 == 0:
            self.updateActions()
        if self._timestep % 20 == 0:
            for player in self._players:
                player.shoot()
        for player in self._players:
            player.update()
        self.checkShots()
        self.checkCollisions()
        self._timestep += 1

        return self._gameState

    def updateActions(self):
        self._player1.updateAction(self._timestep, self._player2.position, self._player2.velocity, self._player2.bullets)
        self._player2.updateAction(self._timestep, self._player1.position, self._player1.velocity, self._player1.bullets)

    def checkShots(self):
        if self._player1.rect.collidelist(self._player2.bullets) != -1:
            print(f"{self._player1.name} was shot!")
            self._gameState = 2
            self._score = (self._score[0], self._score[1] + 1)
        if self._player2.rect.collidelist(self._player1.bullets) != -1:
            print(f"{self._player2.name} was shot!")
            self._gameState = 1
            self._score = (self._score[0] + 1, self._score[1])

    def checkCollisions(self):
        for player in self._players:
            for otherPlayer in self._players:
                if player != otherPlayer:
                    if player.rect.colliderect(otherPlayer.rect):
                        print(f"{player.name} collided with {otherPlayer.name}!")

    def draw(self):
        self._screen.fill((255, 255, 255))
        for player in self._players:
            player.draw(self._screen)
        pygame.display.flip()
