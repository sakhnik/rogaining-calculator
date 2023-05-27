import math


class Position:
    def __init__(self, lat: float = 50.4501, lon: float = 30.5234):
        self.lat: float = lat
        self.lon: float = lon
        self.acc: int = 0

    @classmethod
    def from_dict(cls, data):
        pos = cls()
        pos.lat = data["latitude"]
        pos.lon = data["longitude"]
        pos.acc = data["accuracy"]

    def __str__(self):
        return f"({self.lat}, {self.lon})"

    def distance_to(self, other) -> float:
        # Earth's radius in kilometers
        radius = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(self.lat)
        lon1_rad = math.radians(self.lon)
        lat2_rad = math.radians(other.lat)
        lon2_rad = math.radians(other.lon)

        # Calculate the differences between the coordinates
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        # Apply the Haversine formula
        a = math.sin(delta_lat / 2)**2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Calculate the distance
        distance = radius * c
        return distance
