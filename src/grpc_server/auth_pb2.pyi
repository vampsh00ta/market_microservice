from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserRequest(_message.Message):
    __slots__ = ["jwt_token"]
    JWT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    jwt_token: str
    def __init__(self, jwt_token: _Optional[str] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
