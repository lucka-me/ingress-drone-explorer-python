import math
import time

from explorer.data import ExplorerData
from s2 import Cell

_VISIBLE_RADIUS: float = 500
_REACHABLE_RADIUS_WITH_KEY: float = 1250
_SAFE_ROUNDS_FOR_VISIBLE_RADIUS: int = math.ceil(_VISIBLE_RADIUS / 80)

def explore(data: ExplorerData):
    start_time = time.monotonic_ns()
    start_cell = Cell.from_coordinate(data.start)
    print(f"⏳ Explore from {data.start} in cell #{start_cell}")

    queue: set[Cell] = set()

    if start_cell in data.cells:
        queue.add(start_cell)
    else:
        cells = start_cell.neighbored_cells_covering_cap_of(data.start, _VISIBLE_RADIUS)
        for cell in cells:
            if cell in data.cells:
                queue.add(cell)

    previous_time = start_time
    digits = len(str(len(data.cells)))

    while len(queue) > 0:
        cell = queue.pop()
        portals = data.cells[cell]

        data.reachable_cells.add(cell)
        data.cells_containing_keys.pop(cell, None)

        # Get all neighbors in the visible range (also the possible ones), filter the empty/pending/reached ones and
        # search for reachable ones
        neighbors = cell.neighbored_cells_in(_SAFE_ROUNDS_FOR_VISIBLE_RADIUS)
        for neighbor in neighbors:
            if neighbor in queue or neighbor in data.reachable_cells or neighbor not in data.cells:
                continue
            for portal in portals:
                if neighbor.intersects_with_cap_of(portal.coordinate, _VISIBLE_RADIUS):
                    queue.add(neighbor)
                    break

        # Reach by keys
        # Consider to use cell.neighboredCellsIn instead?
        if len(data.cells_containing_keys) > 0:
            for portal in portals:
                cells_to_remove: set[Cell] = set()
                for target_cell in data.cells_containing_keys:
                    if target_cell in queue:
                        cells_to_remove.add(target_cell)
                        continue
                    keys = data.cells_containing_keys[target_cell]
                    for targe in keys:
                        if portal.coordinate.distance_to(targe.coordinate) \
                            < _REACHABLE_RADIUS_WITH_KEY:
                            queue.add(target_cell)
                            cells_to_remove.add(target_cell)
                            break
                for item in cells_to_remove:
                    del data.cells_containing_keys[item]
                if len(data.cells_containing_keys) == 0:
                    break

        now = time.monotonic_ns()
        if now - previous_time > 1E9:
            print(f"  ⏳ Reached {len(data.reachable_cells):{digits}} / {len(data.cells)} cell(s)")
            previous_time = now

    end_time = time.monotonic_ns()
    print(f"🔍 Exploration finished after {(end_time - start_time) * 1E-9} seconds.")
