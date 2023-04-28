import asyncio
import json
import os
import time
from datetime import datetime
from typing import List

from config import KAFKA_TOPIC, KAFKA_CONSUMER_GROUP, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_DELIVERY
from src.delivery.models import Delivery, DeliveryStatus
from src.delivery.schemas import  DeliveryCreateSchema
from aiokafka import AIOKafkaConsumer

from src.delivery.utils import make_random_track_id
from utils.database import async_session_maker

loop = asyncio.get_event_loop()
consumer =  AIOKafkaConsumer(KAFKA_TOPIC_DELIVERY, group_id=KAFKA_CONSUMER_GROUP,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, loop=loop)


async def consume():
    await consumer.start()
    try:

        async for msg in consumer:
            async with async_session_maker() as session:
                delivery_data = json.loads(msg.value)
                track_id = make_random_track_id(9)
                delivery = Delivery(**delivery_data)
                delivery.track_id = track_id

                delivery_status = DeliveryStatus(current_city=delivery_data['city'], delivery_status_id=1,
                                                 status_update=datetime.utcnow(), track_id=track_id)
                session.add(delivery)
                session.add(delivery_status)
                await session.commit()
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


