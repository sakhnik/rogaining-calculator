from position import Position
from storage import Storage
from defs import format_time, calc_tempo


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
        self.points: int = 0

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

    def calc_penanlty(self, deadline: int):
        # Penalize tardiness
        dt = self.finish - deadline
        if dt > 0:
            return (dt + 59) // 60
        return 0

    def calc_points(self, deadline: int):
        self.points = 0
        visited_codes = set()
        # Count by visited controls
        for p in self.punches:
            if p.code not in visited_codes:
                visited_codes.add(p.code)
                self.points += p.code // 10
        self.points -= self.calc_penanlty(deadline)
        return self.points

    def get_progress_table(self, width: int, start: int, deadline: int,
                           storage: Storage):
        prev_time: int = start
        prev_position: Position = storage.get_start_position()
        points = 0
        distance_km = 0

        table = ["КП    Час    Бали   Км   Темп"]

        def add_leg(code: str, time: int, value: int, position: Position):
            nonlocal prev_time, prev_position, distance_km, points
            nonlocal start, deadline

            leg_km = prev_position.distance_to(position)
            distance_km += leg_km
            points += value
            tempo = calc_tempo(time - prev_time, leg_km)

            table.append(f"{code:3} {format_time(time - start).rjust(7)} {points:4d} {distance_km:5.1f} {tempo.rjust(7)}")
            prev_time, prev_position = time, position

        for idx, punch in enumerate(self.punches):
            add_leg(str(punch.code), punch.time,
                    punch.code // 10,
                    storage.get_control_position(punch.code))
        add_leg("F", self.finish, -self.calc_penanlty(deadline),
                storage.get_finish_position())

        return "\n".join(table)
