import time
import json

import asyncio
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


async def bot(pipeline_name, connect_url):
    async with websockets.connect(connect_url) as websocket:
        await websocket.send(json.dumps({"user": "chatbot", "text": f"model: {pipeline_name}"}))
        await websocket.recv()
