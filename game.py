import pygame, sys


class Brain:
    def getAction(self, myPosition: tuple, myVelocity: tuple,
                  enemyPosition: tuple, enemyVelocity: tuple,
                  closestBulletPosition: tuple) -> tuple:
        '''
        Given a gamestate, return a tuple of ((x, y), (x, y)) to move the player and shoot a bullet.
        '''
        return ((0, 0), (0, 0))


class Bullet:
    def __init__(self, position: tuple, velocity: tuple):
        self._position: tuple = position
        self._velocity: tuple = velocity
        self._size: tuple = (5, 5)
        self._speed: int = 50

    def update(self, area: tuple):
        self._position = (self._position[0] + self._speed * self._velocity[0],
                          self._position[1] + self._speed * self._velocity[1])

    def draw(self, surface):
        pygame.draw.rect(
            surface, (255, 0, 0),
            pygame.Rect(self._position[0], self._position[1], self._size[0],
                        self._size[1]))


class Player:
    def __init__(self, brain: Brain, position: tuple = (0, 0)):
        self._position: tuple = position
        self._velocity: tuple = (10, 10)
        self._name: str = "Player"
        self._size: tuple = (30, 30)
        self._brain: Brain = brain
        self._bullets: list = []
        self._action: tuple = ((0, 0), (0, 0))
        self._speed: int = 10

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

    @name.setter
    def name(self, name: str):
        self._name = name

    @size.setter
    def size(self, size: tuple):
        self._size = size

    def _shoot(self, direction: tuple):
        self._bullets.append(Bullet(self._position, direction))

    def updateAction(self, enemyPosition: tuple, enemyVelocity: tuple, closestBulletPosition: tuple):
        self._action = self._brain.getAction(self._position, self._velocity, enemyPosition,enemyVelocity, closestBulletPosition)
        assert(self._action[0][0] in [-1, 0, 1] and self._action[0][1] in [-1, 0, 1] and self._action[1][0] in [-1, 0, 1] and self._action[1][1] in [-1, 0, 1])
        self._velocity = self._action[0]
        self._shoot(self._action[1])

    def update(self, area: tuple):
        clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        self._position = (clamp(self._position[0] + self._speed * self._velocity[0], 0, area[0] - self._size[0]), clamp(self._position[1] + self._speed * self._velocity[1], 0, area[1] - self._size[1]))
        for bullet in self._bullets:
            bullet.update()
            if bullet.position[0] < 0 or bullet.position[0] > area[0] or bullet.position[1] < 0 or bullet.position[1] > area[1]:
                self._bullets.remove(bullet)

    def draw(self, surface):
        pygame.draw.rect(
            surface, (0, 0, 0),
            pygame.Rect(self._position[0], self._position[1], self._size[0],
                        self._size[1]))
        for bullet in self._bullets:
            bullet.draw(surface)


class Game:
    pass
