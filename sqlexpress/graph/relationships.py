from dataclasses import dataclass

from . import entities as en


@dataclass
class Rship:
    source: en.Entity
    target: en.Entity


@dataclass
class TableToTable(Rship):
    source: en.Table
    target: en.Table
