import asyncio

from fastapi import FastAPI
from src.authv2.router  import router as authv2_router
from src.items.router  import router as items_router
from src.cart.router import router as cart_router



from utils.producer import producer

app = FastAPI(title='Auth microserice')

app.include_router(authv2_router)
app.include_router(cart_router)
app.include_router(items_router)

@app.on_event('startup')
async  def startu_event_producer():
    await producer.start()

@app.on_event('shutdown')
async def start_up():
    await producer.stop()