class Player:
    def __init__(self):
        self._position: tuple = (0, 0)
        self._velocity: tuple = (0, 0)
        self._name: str = "Player"
        self._size: tuple = (10, 10)
    
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
    @name.setter
    def name(self, name: str):  
        self._name = name
    @size.setter
    def size(self, size: tuple):
        self._size = size

    def move(self, x: int, y: int):
        clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        self._velocity = (clamp(x, -3, 3), clamp(y, -3, 3))
    def _update(self):
        self._position = (self._position[0] + self._velocity[0], self._position[1] + self._velocity[1])

class Game:
    pass