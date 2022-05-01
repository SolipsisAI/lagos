import json
import asyncio
import websockets


CONNECTIONS = set()


async def handler(websocket):
    CONNECTIONS.add(websocket)
    try:
        async for message in websocket:
            # Broadcast a message to all connected clients.
            websockets.broadcast(CONNECTIONS, message)
    finally:
        # Unregister.
        CONNECTIONS.remove(websocket)


async def app():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run5eva
