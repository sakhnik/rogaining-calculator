#!/usr/bin/env python

import asyncio
from aiohttp import web, ClientSession
import json
from card import Card
from cards import Cards
from pg_storage import PgStorage
import defs
from printer import Printer


cards = Cards()
storage = PgStorage()
printer = Printer(storage)


def print_receipt(card: Card):
    clname = storage.get_class(card.number)
    print(f"{card.number} {clname}")
    name = storage.get_name(card.number)
    print(f"{name}")
    card.calc_points(defs.deadline)
    print(card.get_progress_table(32, defs.start, defs.deadline, storage))
    print("-" * 32)
    printer.print(card)


async def handle_post(request):
    post_data = await request.read()
    card = Card.from_dict(json.loads(post_data.decode('utf-8')))
    if card.number >= 100:
        # Pass the request along to Quick Event
        async with ClientSession() as session:
            async with session.post(defs.quickevent_url,
                                    data=post_data) as response:
                return web.Response(text=await response.text())
    cards.insert(card.number, post_data.decode('utf-8'))
    print_receipt(card)
    response = web.Response(text='Thanks!')
    return response


async def run_server():
    app = web.Application()
    app.add_routes([web.post('/card', handle_post)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=defs.server_port)
    print(f'Starting server on port {defs.server_port}...')
    await site.start()


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_server())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        cards.close()
