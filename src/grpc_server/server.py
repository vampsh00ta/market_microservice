# from concurrent import futures
#
# import grpc
# from grpclib.utils import graceful_exit
# from grpclib.server import Server
# from src.grpc_server.auth_pb2 import *
# from src.grpc_server.auth_pb2_grpc import GetUserService,GetUserServiceServicer,add_GetUserServiceServicer_to_server,GetUserServiceStub
# from grpc import aio
# from src.authv2.auth import AuthService
# import src.grpc_server.auth_pb2  as pb2
#
# class User(GetUserServiceServicer):
#     # stub = GetUserServiceStub(channel)
#     # response = stub.user
#
#     async def get_user_data(self, request, context):
#         jwt = request.jwt
#         print(jwt)
#         user = AuthService.validate_grpc(jwt)
#         return pb2.GetUserResponse(
#             name = user.name,
#             email = user.email
#
#     )
#
from grpc import aio

import logging

from src.authv2.auth import AuthService

logger = logging.getLogger('foo-logger')

#
# async def start():
#     server = aio.server()
#     pb2_grpc.add_UnaryServicer_to_server(UnaryService(),server)
#     listen_addr = '[::]:50051'
#     server.add_insecure_port(listen_addr)
#     await server.start()
#     await server.wait_for_termination()


import grpc
from concurrent import futures
import time
# import src.grpc_server.protos.unary_pb2_grpc as pb2_grpc
# import src.grpc_server.protos.unary_pb2 as pb2

import src.grpc_server.auth_pb2_grpc as pb2_grpc
import src.grpc_server.auth_pb2 as pb2


# class UnaryService(pb2_grpc.UnaryServicer):
#
#     def __init__(self, *args, **kwargs):
#         pass
#
#     async def GetServerResponse(self, request, context):
#
#         message = request.message
#         result = f'Hello I am up and running received "{message}" message from you'
#         result = {'message': result, 'received': True}
#         print(result)
#         return  pb2.MessageResponse(**result)
class UserService(pb2_grpc.UserServicer):

    def __init__(self, *args, **kwargs):
        pass

    async def GetUser(self, request, context):

        jwt = request.jwt_token

        user = AuthService.validate_grpc(jwt)
        result = {'name': user.username, 'email': user.email}
        return  pb2.UserResponse(**result )
async def serve():
    server = aio.server()
    pb2_grpc.add_UserServicer_to_server(UserService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()