import redis
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL)

CHANNEL = "inventory_updates"

def publish_update(product_id: int, stock: int):
    """
    Publishes an inventory update message to the Redis channel.
    """
    message = json.dumps({"product_id": product_id, "stock": stock})
    r.publish(CHANNEL, message)
    print(f"📤 Published update -> {message}")

async def subscribe_updates():
    """
    Subscribes to the Redis channel asynchronously.
    Listens for real-time inventory updates.
    """
    loop = asyncio.get_event_loop()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)
    print(f"📡 Subscribed to Redis channel: {CHANNEL}")

    # Run in a thread-safe way so it doesn’t block FastAPI
    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = json.loads(message["data"])
            print(f"📥 Received update -> {data}")
        await asyncio.sleep(0.1)  # small delay to prevent blocking
