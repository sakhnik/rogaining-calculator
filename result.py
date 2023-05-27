#!/usr/bin/env python

from pg_storage import PgStorage
from cards import Cards
from card import Card
from defs import deadline
import json
from tabulate import tabulate


storage = PgStorage()

cards = [Card.from_dict(json.loads(c)) for _, c in Cards().read()]

# Partition all the cards by classes
classes: dict[str, [Card]] = {}

for card in cards:
    clname = storage.get_class(card.number)
    classes.setdefault(clname, []).append(card)

# Assign places in every class
for clname, cards in classes.items():
    for card in cards:
        card.calc_points(deadline)
    cards.sort(key=lambda card: card.points, reverse=True)

    print()
    print(f"== {clname} ==")
    table = []
    prev_card = None
    place = 1
    headers = ["№", "Ім’я", "Клуб", "К-ть КП", "Бали", "Місце"]
    for idx, card in enumerate(cards):
        if prev_card and prev_card.points > card.points:
            place += 1
        prev_card = card
        name = storage.get_name(card.number)
        table.append([idx + 1, name, "club",
                      len(card.punches),
                      card.points,
                      place])
    print(tabulate(table, headers=headers))
