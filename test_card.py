from card import Card, Punch


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
