from fastapi import FastAPI
from starlette.requests import Request
# from auth_pb2_grpc import GetUserServiceStub
from src.kafka_consumer.consumer import loop, consume, consumer
from src.delivery.router import router as delivery_router
app = FastAPI()


app.include_router(delivery_router)



@app.on_event("startup")
async def startup_event():
    loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()