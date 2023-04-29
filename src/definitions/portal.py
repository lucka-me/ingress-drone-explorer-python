from definitions.coordinate import Coordinate

class Portal:
    guid: str
    title: str
    coordinate: Coordinate

    def __init__(self, guid: str, title: str, coordinate: Coordinate) -> None:
        self.guid = guid
        self.title = title
        self.coordinate = coordinate

    def __eq__(self, __value: 'Portal') -> bool:
        return self.guid == __value.guid

    def __hash__(self) -> int:
        return hash(self.guid)