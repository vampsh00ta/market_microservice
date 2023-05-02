import asyncio
import json
import os
import time
from typing import List

from redis import redis
from config import KAFKA_TOPIC, KAFKA_CONSUMER_GROUP, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_RECOMMENDATIONS

from aiokafka import AIOKafkaConsumer

from src.recommendations.recs import RecWeigths, recsInit

loop = asyncio.get_event_loop()
consumer =  AIOKafkaConsumer(KAFKA_TOPIC_RECOMMENDATIONS, group_id=KAFKA_CONSUMER_GROUP,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, loop=loop)

async def set_recommendations_to_db(data:dict=None):
    pass
async def consume():
    await consumer.start()
    # redis = anext(get_async_redis())
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            used_id = data.get('user_id',None)
            category= data.get('category',None)
            tags=    data.get('tags',None)
            type = data.get('type',None)
            recs = await recsInit(redis,used_id)
            await recs.add(type= type,category = category,tags=tags)
            user_interac_data =  await recs.get_tags()
            #добавляет ремомедованные товары юзеру
            await set_recommendations_to_db()
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
            # time.sleep(5)

    finally:
        await consumer.stop()


