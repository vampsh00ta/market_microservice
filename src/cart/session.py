from typing import Dict
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.backends.session_backend import SessionModel
from pycparser.c_ast import ID
from pydantic import BaseModel
import aioredis
# class SessionData(BaseModel):
#     username: str
# class CustomSession(InMemoryBackend[UUID, SessionData]):
#     def __init__(self):
#         self.redis = await aioredis.create_redis(address=('redis', 6379))
#         self.data: Dict[ID, SessionModel] = {}
#         await self.redis.
# backend = InMemoryBackend[UUID, SessionData]()