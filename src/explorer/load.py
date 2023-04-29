import json
import time

from io import TextIOWrapper

from definitions.coordinate import Coordinate
from definitions.portal import Portal
from explorer.data import ExplorerData
from s2 import Cell

def load_portals_from(data: ExplorerData, files: list[TextIOWrapper]):
    start_time = time.monotonic_ns()
    print("⏳ Loading Portals...")
    portal_count = 0
    for file in files:
        contents = json.load(file)
        file_add_portal_count = 0
        file_add_cell_count = 0
        for raw in contents:
            coordinate = Coordinate(raw['lngLat']['lng'], raw['lngLat']['lat'])
            portal = Portal(raw['guid'], "" if 'title' not in raw else raw['title'], coordinate)
            cell = Cell.from_coordinate(coordinate)
            if cell not in data.cells:
                data.cells[cell] = { portal }
                file_add_portal_count += 1
                file_add_cell_count += 1
                continue
            portals = data.cells[cell]
            if portal not in portals:
                portals.add(portal)
                file_add_portal_count += 1
            elif len(portal.title) > 0:
                portals.discard(portal)
                portals.add(portal)
        portal_count += file_add_portal_count
        print(
            f"  📃 Added {file_add_portal_count:5} portal(s) and {file_add_cell_count:4} cell(s) "
            f"from {file.name}"
        )

    end_time = time.monotonic_ns()
    print(
        f"📍 Loaded {portal_count} Portal(s) in {len(data.cells)} cell(s) "
        f"from {len(files)} file(s), which took {(end_time - start_time) * 1E-9} seconds."
    )

def load_keys_from(data: ExplorerData, file: TextIOWrapper):
    contents = json.load(file)
    ids: set[Portal] = set()
    for item in contents:
        ids.add(Portal(item, "", Coordinate(0, 0)))
    load_count = len(ids)
    for cell in data.cells:
        keys = data.cells[cell].intersection(ids)
        if len(keys) == 0:
            continue
        ids.difference_update(keys)
        data.cells_containing_keys[cell] = keys
    print(
        f"🔑 Loaded {load_count} Key(s) and matched {load_count - len(ids)} "
        f"in {len(data.cells_containing_keys)} cell(s)."
    )
