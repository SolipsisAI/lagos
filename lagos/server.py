import time
import json

import asyncio
from urllib import response
import websockets

from lagos.pipelines import load_pipeline

CONNECTIONS = set()


def bot_handler(pipeline, event):
    _, conversation = pipeline.predict(text=event["text"])
    response_text = conversation.generated_responses[-1]

    # Show typing
    websockets.broadcast(
        CONNECTIONS, json.dumps({"user": "chatbot", "is_typing": True})
    )
    num_tokens = len(response_text)
    time.sleep(0.1 * num_tokens)

    # Chatbot
    websockets.broadcast(
        CONNECTIONS,
        json.dumps(
            {
                "user": "chatbot",
                "text": response_text,
                "is_typing": False,
            }
        ),
    )


def handler_wrapper(pipeline_name):
    pipeline = load_pipeline(pipeline_name)

    async def handler(websocket):
        CONNECTIONS.add(websocket)

        try:
            async for message in websocket:
                event = json.loads(message)

                # Broadcast a message to all connected clients.
                websockets.broadcast(CONNECTIONS, message)

                bot_handler(pipeline, event=event)
        finally:
            # Unregister.
            CONNECTIONS.remove(websocket)

    return handler


async def app(pipeline_name, host="", port: int = 8001):
    print(f"MODEL: {pipeline_name}")
    async with websockets.serve(handler_wrapper(pipeline_name), host, port):
        print(f"Connect to: ws://{host}:{port}")
        await asyncio.Future()  # run5eva
