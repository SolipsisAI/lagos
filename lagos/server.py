import asyncio
import datetime
import random
import websockets


CONNECTIONS = set()


async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def show_time():
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(random.random() * 2 + 1)


async def app():
    async with websockets.serve(register, "", 8001):
        await show_time()
