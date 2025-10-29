from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
from app.routes.inventory import router as inventory_router
from redis_pubsub import subscribe_updates  # fixed path (assuming redis_pubsub.py is in app/)
# If redis_pubsub.py is in backend/, use: from redis_pubsub import subscribe_updates

app = FastAPI(title="Real-Time Inventory System")

# Include your inventory routes
app.include_router(inventory_router)

@app.on_event("startup")
async def start_listener():
    """
    On startup, run a background Redis subscriber that listens for updates.
    Keeps this FastAPI instance in sync with others in real-time.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(subscribe_updates())

@app.get("/", response_class=HTMLResponse)
def welcome():
    """
    Simple landing page to confirm that the API is running.
    """
    return """
    <html>
        <head>
            <title>Real-Time Inventory API</title>
        </head>
        <body style="font-family:Arial; text-align:center; margin-top:100px;">
            <h1>🚀 Real-Time Inventory API is Running!</h1>
            <p>Use the endpoints under <b>/docs</b> to interact with the API.</p>
        </body>
    </html>
    """
