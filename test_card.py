from card import Card, Punch
from storage import Storage
from position import Position


def test_calc_points():
    card = Card()
    card.finish = 12345
    card.punches.append(Punch(31, 11111))
    card.punches.append(Punch(41, 11200))
    card.punches.append(Punch(51, 11300))
    card.punches.append(Punch(55, 11400))
    card.punches.append(Punch(63, 11500))
    card.punches.append(Punch(68, 11600))
    card.punches.append(Punch(72, 11700))
    card.punches.append(Punch(75, 11800))
    card.punches.append(Punch(84, 11900))
    card.punches.append(Punch(93, 12000))
    assert 60 == card.calc_points(12345)
    assert 59 == card.calc_points(12344)
    assert 59 == card.calc_points(12285)
    assert 58 == card.calc_points(12284)


def test_get_progress_table():
    card = Card()
    card.finish = 11345
    card.punches.append(Punch(31, 11111))
    card.punches.append(Punch(41, 11200))
    card.punches.append(Punch(51, 11300))

    class TestStorage(Storage):
        def __init__(self):
            self.controls = {
                31: Position(50.3825278, 30.4762134),
                41: Position(50.3823938, 30.4711522),
                51: Position(50.3822742, 30.476214)
            }

        def get_start_position(self) -> Position:
            return Position(50.3827041, 30.4706247)

        def get_finish_position(self) -> Position:
            return Position(50.3809636, 30.4719818)

        def get_control_position(self, code: int) -> Position:
            return self.controls[code]

        def get_class(self, number: int) -> str:
            return "cl"

        def get_name(self, number: int) -> str:
            return "John Doe"

    storage = TestStorage()
    table = card.get_progress_table(32, 11000, 11345, storage)
    ref_table = """
КП    Час    Бали   Км   Темп
31    01:51    3   0.4   04:39
41    03:20    7   0.8   04:07
51    05:00   12   1.1   04:38
F     05:45   12   1.4   02:14
"""
    assert table == ref_table.strip()
