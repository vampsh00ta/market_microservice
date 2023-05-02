from fastapi import FastAPI
from starlette.requests import Request
# from auth_pb2_grpc import GetUserServiceStub
from consumer import loop, consume, consumer
from src.grpc_server.grpc_client import grpc_client
from src.recommendations.router import router as router_recommendations
app = FastAPI()


app.include_router(router_recommendations)



@app.on_event("startup")
async def startup_event():
    grpc_client.start()
    # loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    # await consumer.stop()
    pass