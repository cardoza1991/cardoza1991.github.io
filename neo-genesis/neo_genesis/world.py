"""Spatial world: energy field + occupancy."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

@dataclass
class World:
    width: int
    height: int
    regen: float = 0.35
    capacity: float = 10.0

    def __post_init__(self) -> None:
        cap = self.capacity
        self.energy = [[cap for _ in range(self.width)] for _ in range(self.height)]
        self.occ: list[list[Optional[int]]] = [[None for _ in range(self.width)] for _ in range(self.height)]

    def wrap(self, x: int, y: int) -> tuple[int, int]:
        return x % self.width, y % self.height

    def ahead(self, x: int, y: int, heading: int) -> tuple[int, int]:
        dx, dy = DIRS[heading % 4]
        return self.wrap(x + dx, y + dy)

    def vacant(self, x: int, y: int) -> bool:
        x, y = self.wrap(x, y)
        return self.occ[y][x] is None

    def place(self, oid: int, x: int, y: int) -> None:
        x, y = self.wrap(x, y)
        self.occ[y][x] = oid

    def clear(self, x: int, y: int) -> None:
        x, y = self.wrap(x, y)
        self.occ[y][x] = None

    def move(self, oid: int, x0: int, y0: int, x1: int, y1: int) -> bool:
        x1, y1 = self.wrap(x1, y1)
        if self.occ[y1][x1] is not None:
            return False
        self.clear(x0, y0)
        self.place(oid, x1, y1)
        return True

    def pull_energy(self, x: int, y: int, amount: float) -> float:
        x, y = self.wrap(x, y)
        taken = min(amount, self.energy[y][x])
        self.energy[y][x] -= taken
        return taken

    def field_at(self, x: int, y: int) -> float:
        x, y = self.wrap(x, y)
        return self.energy[y][x]

    def occupant(self, x: int, y: int) -> Optional[int]:
        x, y = self.wrap(x, y)
        return self.occ[y][x]

    def tick_field(self) -> None:
        cap, r = self.capacity, self.regen
        for y in range(self.height):
            row = self.energy[y]
            for x in range(self.width):
                if row[x] < cap:
                    row[x] = min(cap, row[x] + r)

    def total_field(self) -> float:
        return sum(sum(row) for row in self.energy)
