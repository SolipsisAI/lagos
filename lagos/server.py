import json
import asyncio
import websockets

from lagos.pipelines import load_pipeline

CONNECTIONS = set()


def bot_handler(pipeline, event):
    _, conversation = pipeline.predict(text=event["text"])
    return conversation.generated_responses[-1]


def handler_wrapper(pipeline_name):
    pipeline = load_pipeline(pipeline_name)

    async def handler(websocket):
        CONNECTIONS.add(websocket)

        try:
            async for message in websocket:
                event = json.loads(message)

                # Broadcast a message to all connected clients.
                websockets.broadcast(CONNECTIONS, message)

                # Show typing
                # TODO: Add a slight, random delay
                websockets.broadcast(CONNECTIONS, json.dumps({
                    "user": "chatbot",
                    "is_typing": True
                }))

                # Chatbot
                response_text = bot_handler(pipeline, event)
                websockets.broadcast(CONNECTIONS, json.dumps({
                    "user": "chatbot",
                    "text": response_text,
                    "is_typing": False,
                }))
        finally:
            # Unregister.
            CONNECTIONS.remove(websocket)

    return handler


async def app(pipeline_name, host="", port: int = 8001):
    print(f"MODEL: {pipeline_name}")
    async with websockets.serve(handler_wrapper(pipeline_name), host, port):
        print(f"Connect to: ws://{host}:{port}")
        await asyncio.Future()  # run5eva
