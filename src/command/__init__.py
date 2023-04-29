import argparse

from definitions.coordinate import Coordinate
from explorer import Explorer

def execute():
    parser = argparse.ArgumentParser(
        prog = "Ingress Drone Explorer",
        description = "An offline CLI tool to analyze reachable Portals for Ingress Drone Mark I.",
    )
    parser.add_argument(
        "portal_list_files",
        help = "Paths of portal list files.",
        metavar = "filename",
        nargs = "+",
        type = argparse.FileType("r", encoding = "utf-8"),
    )
    parser.add_argument(
        "--start",
        "-s",
        dest = "start",
        help = "The starting point.",
        metavar = "<longitude,latitude>",
        nargs = 1,
        required = True,
        type = Coordinate.from_string,
    )
    parser.add_argument(
        "--key-list",
        "-k",
        dest = "key_list_file",
        help = "Path of key list file.",
        metavar = "filename",
        nargs = 1,
        type = argparse.FileType("r", encoding = "utf-8"),
    )
    parser.add_argument(
        "--output-drawn-items",
        dest = "output_drawn_items_file",
        help = "Path of drawn items file to output.",
        metavar = "filename",
        nargs = 1,
        type = argparse.FileType("w", encoding = "utf-8"),
    )
    args = parser.parse_args()
    explorer = Explorer()
    explorer.load_portals_from(args.portal_list_files)
    if args.key_list_file is not None:
        explorer.load_keys_from(args.key_list_file[0])
    explorer.explore_from(args.start[0])
    explorer.report()
    if args.output_drawn_items_file is not None:
        explorer.save_drawn_items_to(args.output_drawn_items_file[0])
