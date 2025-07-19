from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os
from app.routes.video_process import video_process, ProcessRequest


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS")
TOPIC = "video.process.start"

async def handle_message(data: dict):
    print("[Kafka] New job:", data)

    try:
        donor = data["donor"]
        video_metadata = data["videoMetadata"]

        request_obj = ProcessRequest(
            donor_id=donor.get("id"),
            first_name=donor.get("first_name"),
            last_name=donor.get("last_name"),
            video_link=video_metadata.get("url")
        )

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, video_process, request_obj)

        print("[Kafka] Video processing result:", result)

        await kafka_producer_service.send("video.process.done", {
    "videoId": public_id,
    "blurUrl": result.get("blurred_video_url"),
    "enhancedUrl": result.get("enhanced_video_url", "") 
})

    except Exception as e:
        print("[Kafka] Error processing message:", str(e))
        await kafka_producer_service.send("video.process.error", {
    "error": str(e),
    "payload": data
})



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
