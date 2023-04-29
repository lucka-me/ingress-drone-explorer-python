from io import TextIOWrapper
import json

from definitions.portal import Portal
from explorer.data import ExplorerData

def report(data: ExplorerData):
    portals_count = 0
    reachable_portals_count = 0
    furthest_portal = Portal("", "", data.start)
    for cell in data.cells:
        portals = data.cells[cell]
        portals_count += len(portals)
        if cell not in data.reachable_cells:
            continue
        reachable_portals_count += len(portals)
        for portal in portals:
            if data.start.closer(furthest_portal.coordinate, portal.coordinate):
                furthest_portal = portal
    if reachable_portals_count == 0:
        print(f"⛔️ There is no reachable portal in {portals_count} portal(s) from ${data.start}")
        return

    total_number_digits = len(str(portals_count))
    reachable_number_digits = len(str(reachable_portals_count))
    unreachable_number_digits = len(str(portals_count - reachable_portals_count))

    print(
        f"⬜️ In {len(data.cells):{total_number_digits}}   cell(s), "
        f"{len(data.reachable_cells):{reachable_number_digits}} are ✅ reachable, "
        f"{len(data.cells) - len(data.reachable_cells):{unreachable_number_digits}} are ⛔️ not."
    )
    print(
        f"📍 In {portals_count:{total_number_digits}} Portal(s), "
        f"{reachable_portals_count:{reachable_number_digits}} are ✅ reachable, "
        f"{portals_count - reachable_portals_count:{unreachable_number_digits}} are ⛔️ not."
    )
    print(
        "🛬 The furthest Portal is " +
        (furthest_portal.title if len(furthest_portal.title) > 0 else "Untitled") +
        "."
    )
    print(f"  📍 It's located at {furthest_portal.coordinate}")
    print(f"  📏 Where is {data.start.distance_to(furthest_portal.coordinate) * 1E-3} km away")
    print(
        f"  🔗 Check it out: https://intel.ingress.com/?pll="
        f"{furthest_portal.coordinate.lat},{furthest_portal.coordinate.lng}"
    )

def save_drawn_items_to(data: ExplorerData, file: TextIOWrapper):
    items = [ ]
    for cell in data.cells:
        shape = cell.shape()
        lat_lngs = [ ]
        for point in shape:
            lat_lngs.append({ "lng": point.lng, "lat": point.lat })
        items.append({
            "type": "polygon",
            "color": "#783cbd" if cell in data.reachable_cells else "#404040",
            "latLngs": lat_lngs
        })
    json.dump(items, fp = file)
    print(f"💾 Saved drawn items to {file.name}.")
