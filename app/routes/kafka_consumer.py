from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS")
TOPIC = "video.process.start"

async def handle_message(data: dict):
    print("[Kafka] New job:", data)
    # Trigger AI pipeline here
    # Example: await process_video(data['video_url'])

async def start_consumer():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="ai-processing-consumer",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await handle_message(msg.value)
    finally:
        await consumer.stop()
