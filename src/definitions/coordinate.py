import math

_EARTH_RADIUS = 6371008.8

class Coordinate:
    lng: float
    lat: float

    def __init__(self, lng: float, lat: float) -> None:
        self.lng = lng
        self.lat = lat

    def __str__(self) -> str:
        return f"{self.lng},{self.lat}"

    @classmethod
    def from_string(cls, string: str) -> 'Coordinate':
        pair = string.split(",")
        if len(pair) != 2:
            raise ValueError("Invalid format of coordinate")
        return cls(float(pair[0]), float(pair[1]))

    def closer(self, a: 'Coordinate', b: 'Coordinate') -> bool:
        d_a = (self.lng - a.lng) * (self.lng - a.lng) + (self.lat - a.lat) * (self.lat - a.lat)
        d_b = (self.lng - b.lng) * (self.lng - b.lng) + (self.lat - b.lat) * (self.lat - b.lat)
        return d_a < d_b

    def distance_to(self, other: 'Coordinate') -> float:
        sin_theta = math.sin((other.theta() - self.theta()) / 2)
        sin_phi = math.sin((other.phi() - self.phi()) / 2)
        a = sin_phi * sin_phi + sin_theta * sin_theta * math.cos(self.phi()) * math.cos(other.phi())
        return math.atan2(math.sqrt(a), math.sqrt(1.0 - a)) * 2 * _EARTH_RADIUS

    def distance_to_line(self, a: 'Coordinate', b: 'Coordinate') -> float:
        c1 = (b.lat - a.lat) * (self.lat - a.lat) + (b.lng - a.lng) * (self.lng - a.lng)
        if c1 <= 0:
            return self.distance_to(a)
        c2 = (b.lat - a.lat) * (b.lat - a.lat) + (b.lng - a.lng) * (b.lng - a.lng)
        if c2 <= c1:
            return self.distance_to(b)
        ratio = c1 / c2
        return self.distance_to(
            Coordinate(a.lng + ratio * (b.lng - a.lng), a.lat + ratio * (b.lat - a.lat))
        )

    def phi(self) -> float:
        return self.lat * math.pi / 180.0

    def theta(self) -> float:
        return self.lng * math.pi / 180.0
