import json

import asyncio
import websockets

CONNECTIONS = set()


async def handler(websocket):
    CONNECTIONS.add(websocket)

    try:
        async for message in websocket:
            event = json.loads(message)

            # Broadcast a message to all connected clients.
            websockets.broadcast(CONNECTIONS, json.dumps(event))
    finally:
        # Unregister.
        CONNECTIONS.remove(websocket)


async def app(host="", port: int = 8001):
    async with websockets.serve(handler, host, port):
        print(f"Connect to: ws://{host}:{port}")
        await asyncio.Future()  # run5eva
