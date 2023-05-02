import json
from aioredis import Redis


async def recsInit(redis:Redis,user_id:int):
    recs = RecWeigths(redis, user_id)
    await recs.init()
    return recs
class RecWeigths:
    def __init__(self,redis:Redis,user_id:int):
        self._redis = redis
        self.user_id = user_id
    async def init(self):
        recs = await self._redis.get(f'recs_user_{self.user_id}')
        if recs:
            recs = json.loads(recs)
        else:
            recs = {"likes": {}, 'clicks': {}, 'purchases': {}, 'search': []}
        self.recs = recs
    async def add(self,type:str,category:str,tags:list):

        tag = ''
        tags_output = set(tags)
        for name in tags:

            tag +=name + ' '
            tags_output.add(tag.rstrip(' '))
        print(tags, tags_output)

        if type == 'search':
            self.recs[type] = set(self.recs[type])

            self.recs[type] = list(self.recs[type].union(tags_output))
            await self.save()
            return
        if category not in self.recs[type]:
            self.recs[type][category] = tags_output
        else:
            self.recs[type][category] =   set(self.recs[type][category])
            self.recs[type][category].union(tags_output)
        self.recs[type][category] = list(self.recs[type][category])
        await self.save()
    async def get_tags(self):
        return self.recs
    async def save(self):

        recs = json.dumps(self.recs).encode('utf-8')
        await self._redis.set(f'recs_user_{self.user_id}',recs)