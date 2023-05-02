import asyncio

from fastapi import FastAPI
from src.authv2.router  import router as authv2_router
from src.grpc_server.server import grpc_server
from src.items.router  import router as items_router
from src.cart.router import router as cart_router
from fastapi.middleware.cors import CORSMiddleware


from utils.producer import producer

app = FastAPI(title='Auth microserice')

app.include_router(authv2_router)
app.include_router(cart_router)
app.include_router(items_router)

origins = ["localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async  def startu_event_producer():
    await grpc_server.start_serving()
    await producer.start()

@app.on_event('shutdown')
async def start_up():
    await grpc_server.stop_serving()

    await producer.stop()