from definitions.coordinate import Coordinate
from definitions.portal import Portal
from s2 import Cell

class ExplorerData:
    start = Coordinate(0, 0)
    cells: dict[Cell, set[Portal]] = { }
    reachable_cells: set[Cell] = set()
    cells_containing_keys: dict[Cell, set[Portal]] = { }
