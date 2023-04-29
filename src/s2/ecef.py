import math

from definitions.coordinate import Coordinate

class ECEFCoordinate:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_coordinate(cls, coordinate: Coordinate) -> 'ECEFCoordinate':
        theta = coordinate.theta()
        phi = coordinate.phi()
        cos_phi = math.cos(phi)
        return cls(math.cos(theta) * cos_phi, math.sin(theta) * cos_phi, math.sin(phi))

    @classmethod
    def from_face_s_t(cls, face: int, s: float, t: float) -> 'ECEFCoordinate':
        u = (1.0 / 3.0) * ((4.0 * s * s - 1) if s >= 0.5 else (1.0 - (4.0 * (1.0 - s) * (1.0 - s))))
        v = (1.0 / 3.0) * ((4.0 * t * t - 1) if t >= 0.5 else (1.0 - (4.0 * (1.0 - t) * (1.0 - t))))
        x = 0.0
        y = 0.0
        z = 0.0
        if face == 0: x =  1; y =  u; z =  v
        elif face == 1: x = -u; y =  1; z =  v
        elif face == 2: x = -u; y = -v; z =  1
        elif face == 3: x = -1; y = -v; z = -u
        elif face == 4: x =  v; y = -1; z = -u
        elif face == 5: x =  v; y =  u; z = -1
        return cls(x, y, z)

    def coordinate(self) -> Coordinate:
        return Coordinate(
            math.atan2(self.y, self.x) / math.pi * 180.0,
            math.atan2(self.z, math.sqrt(self.x * self.x + self.y * self.y)) / math.pi * 180.0
        )

    def face_s_t(self) -> tuple[int, float, float]:
        abs_x = abs(self.x)
        abs_y = abs(self.y)
        face = (0 if abs_x > abs(self.z) else 2) \
            if abs_x > abs_y else (1 if abs_y > abs(self.z) else 2)
        if (face == 0 and self.x < 0) or (face == 1 and self.y < 0) or (face == 2 and self.z < 0):
            face += 3
        s = 0.0
        t = 0.0
        if face == 0: s =  self.y / self.x; t =  self.z / self.x
        elif face == 1: s = -self.x / self.y; t =  self.z / self.y
        elif face == 2: s = -self.x / self.z; t = -self.y / self.z
        elif face == 3: s =  self.z / self.x; t =  self.y / self.x
        elif face == 4: s =  self.z / self.y; t = -self.x / self.y
        elif face == 5: s = -self.y / self.z; t = -self.x / self.z
        s = (0.5 * math.sqrt(1 + 3 * s)) if s >= 0 else (1.0 - 0.5 * math.sqrt(1 - 3 * s))
        t = (0.5 * math.sqrt(1 + 3 * t)) if t >= 0 else (1.0 - 0.5 * math.sqrt(1 - 3 * t))
        return face, s, t