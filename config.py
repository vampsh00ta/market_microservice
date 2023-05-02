import smtplib

import aioredis
from dotenv import load_dotenv
import os
load_dotenv()

DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
SECRET=os.environ.get('SECRET')
REDIS_URL = os.environ.get('REDIS_URL')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC_RECOMMENDATIONS = os.getenv('KAFKA_TOPIC_RECOMMENDATIONS')
