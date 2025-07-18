from aiokafka import AIOKafkaProducer
import asyncio
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS")
TOPIC = "video.process.start"

class KafkaProducerService:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send(self, topic: str, message: dict):
        if self.producer is None:
            raise Exception("Producer not started")
        await self.producer.send_and_wait(topic, message)


kafka_producer_service = KafkaProducerService()
