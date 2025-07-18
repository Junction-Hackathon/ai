from fastapi import FastAPI
from .routes.ask import router
from .routes.video_process import video_process_router
import gc

app = FastAPI()

app.include_router(router)
app.include_router(video_process_router)


@app.get("/")
@app.head("/")
def root():
    return {"message": "server is running"}


# @app.middleware("http")
# async def cleanup_middleware(request, call_next):
#     """Clean up memory after each request"""
#     response = await call_next(request)
#     gc.collect()
#     return response
