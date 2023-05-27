#!/usr/bin/env python

import asyncio
from aiohttp import web
import json
from card import Card


PORT=12345


async def handle_post(request):
    post_data = await request.read()
    card = Card.from_dict(json.loads(post_data.decode('utf-8')))
    print(card)
    response = web.Response(text='Thanks!')
    return response


async def run_server():
    app = web.Application()
    app.add_routes([web.post('/card', handle_post)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=PORT)
    print(f'Starting server on port {PORT}...')
    await site.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server())
    loop.run_forever()
