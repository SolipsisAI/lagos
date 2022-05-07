import time
import json
import random

import websockets
from uuid import uuid4

from lagos.pipelines import load_pipeline


async def bot_handler(websocket, pipeline, event, bot_id):
    _, conversation = pipeline.predict(text=event["text"])
    response_text = conversation.generated_responses[-1]

    # Show typing
    await websocket.send(json.dumps({"user_id": bot_id, "is_typing": True}))
    num_tokens = len(response_text)
    time.sleep(0.1 * num_tokens)

    # Send response
    await websocket.send(
        json.dumps(
            {
                "user_id": bot_id,
                "text": response_text,
                "is_typing": False,
            }
        )
    )


async def bot(pipeline_name, connect_url, model=None):
    pipeline = load_pipeline(pipeline_name, model=model)
    bot_id = str(uuid4())
    print(f"Loading {pipeline_name} ({model}) -> connecting to {connect_url}")
    async with websockets.connect(connect_url) as websocket:
        async for message in websocket:
            event = json.loads(message)
            if event.get("user_id") != bot_id and "text" in event:
                # TODO: Use a queue
                time.sleep(random.randint(1,10))
                await bot_handler(
                    websocket, pipeline=pipeline, event=event, bot_id=bot_id
                )
