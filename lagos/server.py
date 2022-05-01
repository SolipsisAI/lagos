import asyncio
import websockets


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)


async def app():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever
