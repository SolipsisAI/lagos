import time
import json

import asyncio
import websockets

from lagos.pipelines import load_pipeline

BOT_USER = "chatbot"


async def bot_handler(websocket, pipeline, event):
    _, conversation = pipeline.predict(text=event["text"])
    response_text = conversation.generated_responses[-1]

    # Show typing
    await websocket.send(
        json.dumps({"user": BOT_USER, "is_typing": True})
    )
    num_tokens = len(response_text)
    time.sleep(0.1 * num_tokens)

    # Send response
    await websocket.send(
        json.dumps(
            {
                "user": BOT_USER,
                "text": response_text,
                "is_typing": False,
            }
        )
    )


async def bot(pipeline_name, connect_url):
    pipeline = load_pipeline(pipeline_name)
    async with websockets.connect(connect_url) as websocket:
        async for message in websocket:
            event = json.loads(message)
            if event["user"] != BOT_USER:
                await bot_handler(websocket, pipeline, event)
            await websocket.recv()
