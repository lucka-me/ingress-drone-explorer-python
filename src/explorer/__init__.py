from io import TextIOWrapper

from definitions.coordinate import Coordinate

from explorer.data import ExplorerData
import explorer.load
import explorer.explore
import explorer.report

class Explorer:
    _data = ExplorerData()

    def load_portals_from(self, files: list[TextIOWrapper]):
        explorer.load.load_portals_from(self._data, files)

    def load_keys_from(self, file: TextIOWrapper):
        explorer.load.load_keys_from(self._data, file)

    def explore_from(self, start: Coordinate):
        self._data.start = start
        explorer.explore.explore(self._data)

    def report(self):
        explorer.report.report(self._data)

    def save_drawn_items_to(self, file: TextIOWrapper):
        explorer.report.save_drawn_items_to(self._data, file)