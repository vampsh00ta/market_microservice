import json

from aiokafka import AIOKafkaProducer
import asyncio

from config import KAFKA_BOOTSTRAP_SERVERS

loop = asyncio.get_event_loop()
def json_serializer(data):
    return json.dumps(data).encode('utf-8')
producer = AIOKafkaProducer(loop = loop,bootstrap_servers = [KAFKA_BOOTSTRAP_SERVERS] ,value_serializer=json_serializer)



