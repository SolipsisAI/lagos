import json
import asyncio
import websockets

from lagos.pipelines import load_pipeline

CONNECTIONS = set()


def bot_handler(pipeline, message):
    _, conversation = pipeline.predict(text=message)
    return conversation.generated_responses[-1]


def handler_wrapper(pipeline_name):
    pipeline = load_pipeline(pipeline_name)

    async def handler(websocket):
        CONNECTIONS.add(websocket)
        conversation_id = None

        try:
            async for message in websocket:
                # Broadcast a message to all connected clients.
                websockets.broadcast(CONNECTIONS, message)
                response = bot_handler(pipeline, message)
                websockets.broadcast(CONNECTIONS, response)
        finally:
            # Unregister.
            CONNECTIONS.remove(websocket)

    return handler


async def app(pipeline_name, host="", port: int = 8001):
    print(f"MODEL: {pipeline_name}")
    async with websockets.serve(handler_wrapper(pipeline_name), host, port):
        print(f"Connect to: ws://{host}:{port}")
        await asyncio.Future()  # run5eva
