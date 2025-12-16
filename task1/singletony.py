
from typing import Any


class DeviceManager:
    ...

device_manager = DeviceManager()

# ------

class DeviceManager2:
    def __init__(self) -> None:
        self.comnnections = {}
    
    def get_connection(self, address):
        if address not in self.comnnections:
            self.comnnections[address] = ...
        return self.comnnections[address]


class DeviceManager3:
    managers = {}
    def __init__(self, address) -> None:
        ...
    
    @classmethod
    def get_manager(cls, address):
        if address not in cls.managers:
            cls.managers[address] = cls(address)
        return cls.managers[address]


class Borg1:
    _shared_state: dict[str, Any] = {}

    def __init__(self) -> None:
        self.__dict__ = self._shared_state


class Borg2:
    _state = {}
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.__dict__ = cls._state
        return instance


# Flyweight

class GameSquare:
    def __init__(self, color) -> None:
        self.color = color
        self.items: list[tuple[int, int]] = []

class GameOfLife:
    def __init__(self) -> None:
        # self.black_squares: list[tuple[int, int]] = []
        # self.white_squares: list[tuple[int, int]] = []
        self.black_squares = GameSquare('black')
        self.white_squares = GameSquare('white')
