# import auth_pb2 as pb2
import grpc
from src.grpc_server import  auth_pb2 as pb2, auth_pb2_grpc as pb2_grpc


class UserClient(object):
    # _instances = {}
    #
    # # def __call__(cls, *args, **kwargs):
    # #     if cls not in cls._instances:
    # #         cls._instances[cls] = super(UserClient, cls).__call__(*args, **kwargs)
    # #     return cls._instances[cls]


    def start(self):
        self.host = 'localhost'
        self.server_port = 50051

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        self.stub = pb2_grpc.UserStub(self.channel)
    def get_user_data(self, jwt_token):
        message = pb2.UserRequest(jwt_token=jwt_token)
        print(message)
        return self.stub.GetUser(message)
grpc_client = UserClient()