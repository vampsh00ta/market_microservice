
from grpc import aio

import logging

from src.authv2.auth import AuthService, get_current_user_or_pass

logger = logging.getLogger('foo-logger')



import src.grpc_server.auth_pb2_grpc as pb2_grpc
import src.grpc_server.auth_pb2 as pb2


class UserService(pb2_grpc.UserServicer):

    def __init__(self, *args, **kwargs):
        pass

    async def GetUser(self, request, context):


        jwt = request.jwt_token

        user = await get_current_user_or_pass(jwt)
        result = {'id': user.id}
        return  pb2.UserResponse(id = user.id )
class GrpcServer():
    def __init__(self):
        self.server = aio.server()
        pb2_grpc.add_UserServicer_to_server(UserService(), self.server)
        listen_addr = '[::]:50051'
        self.server.add_insecure_port(listen_addr)
    async def start_serving(self):
        await self.server.start()
    async def stop_serving(self):
        await self.server.stop(None)
grpc_server = GrpcServer()