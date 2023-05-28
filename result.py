#!/usr/bin/env python

from pg_storage import PgStorage
from cards import Cards
from card import Card
import defs
import json
from tabulate import tabulate


storage = PgStorage()

cards = [Card.from_dict(json.loads(c)) for _, c in Cards().read()]

# Partition all the cards by classes
classes: dict[str, [Card]] = {}

for card in cards:
    clname = storage.get_class(card.number)
    classes.setdefault(clname, []).append(card)


def sort_key(card):
    return (card.points, -card.finish)


# Assign places in every class
for clname, cards in classes.items():
    for card in cards:
        card.calc_points(defs.deadline)
    cards.sort(key=sort_key, reverse=True)

    print()
    print(f"== {clname} ==")
    table = []
    prev_card = None
    place = 1
    headers = ["№", "Ім’я", "Клуб", "К-ть КП", "Бали", "Фініш", "Місце"]
    for idx, card in enumerate(cards):
        if prev_card and sort_key(prev_card) > sort_key(card):
            place = idx + 1
        prev_card = card
        name = storage.get_name(card.number)
        table.append([idx + 1, name, "club",
                      len(card.punches),
                      card.points,
                      defs.format_time(card.finish - defs.start),
                      place])
    print(tabulate(table, headers=headers))
