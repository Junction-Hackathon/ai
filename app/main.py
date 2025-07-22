from fastapi import FastAPI
from .routes.ask import router
from .routes.video_process import video_process_router
from .routes.kafka_consumer import start_consumer
from .routes.kafka_producer import kafka_producer_service

from aiokafka import AIOKafkaConsumer,AIOKafkaProducer

app = FastAPI()

app.include_router(router)
app.include_router(video_process_router)


# @app.on_event("startup")
# async def startup():
#     await kafka_producer_service.start()
#     await start_consumer()

# @app.on_event("shutdown")
# async def shutdown():
#     await kafka_producer_service.stop()
#     await start_consumer()



@app.get("/")
@app.head("/")
async def root():
    consumer = AIOKafkaConsumer(
        "video.process.start.",
        bootstrap_servers="127.0.0.1:29092",
        group_id="ai-processing-consumer",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(msg.value)
    finally:
        await consumer.stop()

    return {"message": "server is running"}


