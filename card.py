from position import Position
from storage import Storage
from tabulate import tabulate


def format_time(time: int) -> str:
    seconds = int(time) % 60
    minutes = int(time // 60)
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def calc_tempo(time: int, distance_km: float) -> str:
    if distance_km == 0:
        return "INF"
    tempo = float(time) / distance_km
    return format_time(int(tempo))


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

    def calc_penanlty(self, deadline: int):
        # Penalize tardiness
        dt = self.finish - deadline
        if dt > 0:
            return (dt + 59) // 60
        return 0

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
        points -= self.calc_penanlty(deadline)
        return points

    def get_progress_table(self, width: int, start: int, deadline: int,
                           storage: Storage):
        headers = ["КП", "Час", "Бали", "Км", "Темп"]
        maxcolwidths = [3, 7, 2, 5, 10]
        table = []
        prev_time: int = start
        prev_position: Position = storage.get_start_position()
        points = 0
        distance_km = 0

        def add_leg(code: str, time: int, value: int, position: Position):
            nonlocal prev_time, prev_position, distance_km, points
            nonlocal start, deadline

            leg_km = prev_position.distance_to(position)
            distance_km += leg_km
            points += value
            tempo = calc_tempo(time - prev_time, leg_km)
            table.append([code,
                          format_time(time - start),
                          points,
                          f"{distance_km:.1f}",
                          tempo])
            prev_time, prev_position = time, position

        for idx, punch in enumerate(self.punches):
            add_leg(punch.code, punch.time,
                    punch.code // 10,
                    storage.get_control_position(punch.code))
        add_leg("F", self.finish, -self.calc_penanlty(deadline),
                storage.get_finish_position())

        table = tabulate(table, headers=headers, tablefmt="plain",
                         maxcolwidths=maxcolwidths)
        return table
