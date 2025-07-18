from fastapi import FastAPI
from .routes.ask import router
from .routes.video_process import video_process_router
from .routes.kafka_consumer import start_consumer
from .routes.kafka_producer import kafka_producer_service
import asyncio

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_consumer())
    await kafka_producer_service.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer_service.stop()

app.include_router(router)
app.include_router(video_process_router)


@app.get("/")
@app.head("/")
def root():
    return {"message": "server is running"}


