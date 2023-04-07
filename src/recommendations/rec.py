import json

from aioredis import Redis

from src.authv2.models import User
from src.authv2.schemas import UserRead

async def recsInit(redis:Redis,user:User):
    recs = RecWeigths(redis, user)
    await recs.init()
    return recs
class RecWeigths:
    def __init__(self,redis:Redis,user:User):
        self._redis = redis
        self.user = user

    async def init(self):
        recs = await self._redis.get(f'recs_user_{self.user.id}')
        if  recs:
            recs =  json.loads(recs)
        else:
            recs = {"likes":{},'clicks':{},'purchases':{},'search':{}}
        self.recs = recs
    async def add(self,type:str,category:str,brand:str,item_name:str):
        tags = set()
        tags.add(brand)
        item_name_split = item_name.split(' ')
        tag = ''
        for name in item_name_split:
            tag +=name + ' '
            tags.add(tag.rstrip(' '))
            tags.add(name.rstrip(' '))

        if category not in self.recs[type]:
            self.recs[type][category] = tags
        else:
            self.recs[type][category] =   set(self.recs[type][category])
            self.recs[type][category].union(tags)
        self.recs[type][category] = list(self.recs[type][category])
        await self.save()
    # async def remove(self,type,category:str,name:str):
    #     self.recs[type].remove(
    #         {
    #             category:name.split(' ')
    #         }
    #     )

    async def save(self):

        recs = json.dumps(self.recs).encode('utf-8')
        await self._redis.set(f'recs_user_{self.user.id}',recs)





