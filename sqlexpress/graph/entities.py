from abc import ABC
from dataclasses import dataclass


@dataclass
class Entity(ABC):
    name: str = None
    alias: str = None


@dataclass
class Table(Entity):
    pass


@dataclass
class Column(Entity):
    pass