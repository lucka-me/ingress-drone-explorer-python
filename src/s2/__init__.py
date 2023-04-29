import math

from definitions.coordinate import Coordinate
from s2.ecef import ECEFCoordinate

class Cell:
    _face: int
    _level: int
    _i: int
    _j: int

    def __init__(self, face: int, i: int, j: int, level: int = 16) -> None:
        self._level = level
        upper = 1 << level
        if i >= 0 and j >= 0 and i < upper and j < upper:
            self._face = face
            self._i = i
            self._j = j
            return
        self._face, s, t = ECEFCoordinate(face, (0.5 + i) / upper, (0.5 + j) / upper).face_s_t()
        self._i = Cell.clamp(math.floor(s * upper), upper - 1, 0)
        self._j = Cell.clamp(math.floor(t * upper), upper - 1, 0)

    def __eq__(self, __value: 'Cell') -> bool:
        return self._face == __value._face and self._level == __value._level    \
            and self._i == __value._i and self._j == __value._j

    def __hash__(self) -> int:
        return hash((self._face, self._level, self._i, self._j))

    def __str__(self) -> str:
        return f"{self._face},{self._level},{self._i},{self._j}"

    @classmethod
    def from_coordinate(cls, coordinate: Coordinate, level: int = 16) -> 'Cell':
        face, s, t = ECEFCoordinate.from_coordinate(coordinate).face_s_t()
        upper = 1 << level
        return cls(
            face,
            Cell.clamp(math.floor(s * upper), 0, upper - 1),
            Cell.clamp(math.floor(t * upper), 0, upper - 1),
            level
        )

    @classmethod
    def clamp(cls, num: int, lower: int, upper: int) -> int:
        return max(min(num, upper), lower)

    def coordinate(self, dI: float, dJ: float) -> Coordinate:
        upper = 1 << self._level
        return ECEFCoordinate.from_face_s_t(
            self._face, (dI + self._i) / upper, (dJ + self._j) / upper
        ).coordinate()

    def intersects_with_cap_of(self, center: Coordinate, radius: float) -> bool:
        corners = self.shape()
        corners.sort(key = center.distance_to)
        return center.distance_to(corners[0]) < radius \
            or center.distance_to_line(corners[0], corners[1]) < radius

    def neighbored_cells_covering_cap_of(self, center: Coordinate, radius: float) -> set['Cell']:
        result: set[Cell] = set()
        outside: set[Cell] = set()
        queue = { self }
        while len(queue) > 0:
            cell = queue.pop()
            if cell in result or outside:
                continue
            if cell.intersects_with_cap_of(center, radius):
                neighbors = self.neighbors()
                for neighbor in neighbors:
                    queue.add(neighbor)
                result.add(cell)
            else:
                outside.add(cell)
        return result

    def neighbored_cells_in(self, rounds: int) -> set['Cell']:
        result: set[Cell] = set()
        for round in range(rounds):
            for step in range((round + 1) * 2):
                result.add(
                    Cell(self._face, self._i - round - 1   , self._j - round + step, self._level)
                )
                result.add(
                    Cell(self._face, self._i - round + step, self._j + round + 1   , self._level)
                )
                result.add(
                    Cell(self._face, self._i + round + 1   , self._j + round - step, self._level)
                )
                result.add(
                    Cell(self._face, self._i + round - step, self._j - round - 1   , self._level)
                )
        return result

    def neighbors(self) -> list['Cell']:
        return [
            Cell(self._face, self._i - 1, self._j       , self._level),
            Cell(self._face, self._i    , self._j - 1   , self._level),
            Cell(self._face, self._i + 1, self._j + 1   , self._level),
            Cell(self._face, self._i    , self._j       , self._level)
        ]

    def shape(self) -> list[Coordinate]:
        return [
            self.coordinate(0, 0),
            self.coordinate(0, 1),
            self.coordinate(1, 1),
            self.coordinate(1, 0),
        ]