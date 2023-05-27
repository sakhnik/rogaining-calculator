
class Position:
    def __init__(self):
        self.lat: float = 0
        self.lon: float = 0
        self.acc: int = 0

    @classmethod
    def from_dict(cls, data):
        pos = cls()
        pos.lat = data["latitude"]
        pos.lon = data["longitude"]
        pos.acc = data["accuracy"]


class Punch:
    def __init__(self, code: int = 0, time: int = 0):
        self.code: int = code
        self.time: int = time
        self.position: Position = None

    @classmethod
    def from_dict(cls, data):
        punch = cls()
        punch.code = data["code"]
        punch.time = data["time"]
        try:
            punch.position = Position.from_dict(data["position"])
        except KeyError:
            pass
        return punch


class Card:
    def __init__(self):
        self.number: int = None
        self.check: int = 0
        self.start: int = 0
        self.finish: int = 0
        self.punches: [Punch] = []

    @classmethod
    def from_dict(cls, data):
        card = cls()
        card.number = data["cardNumber"]
        card.check = data["checkTime"]
        card.start = data["startTime"]
        card.finish = data["finishTime"]
        for p in data["punches"]:
            card.punches.append(Punch.from_dict(p))
        return card

    def calc_points(self, deadline: int):
        points = 0
        visited_codes = set()
        # Count by visited controls
        for p in self.punches:
            if p.code == 10 or p.code == 900:
                continue
            if p.code not in visited_codes:
                visited_codes.add(p.code)
                points += p.code // 10
        # Penalize lateness
        dt = self.finish - deadline
        if dt > 0:
            points -= (dt + 59) // 60
        return points
