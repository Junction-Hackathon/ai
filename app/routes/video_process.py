
import sys
from pydantic import BaseModel
from fastapi import APIRouter
import requests
import os
from concurrent.futures import ProcessPoolExecutor
from dotenv import load_dotenv

import cloudinary
import cloudinary.uploader

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../object_detector/scripts")
    )
)

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../mention-detector/scritps")
    )
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../blood-detector"))
)
from video_checker import check_video_for_sacrifice_animal
from mention import detect_donor_name
from detector import blur

load_dotenv()

video_process_router = APIRouter()


class ProcessRequest(BaseModel):
    donor_id: str
    first_name: str
    last_name: str
    video_link: str


def get_cloudinary_public_id(video_link: str) -> str:
    return video_link.split("/")[-1].split(".")[0]


@video_process_router.post("/process-video")
def video_process(req: ProcessRequest):
    print("processing video...")
    public_id = get_cloudinary_public_id(req.video_link)
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    response = requests.get(req.video_link, auth=(api_key, api_secret))
    
    if response.status_code == 200:
        os.makedirs("videos", exist_ok=True)
        video_path = f"videos/{public_id}.mp4"
        with open(video_path, "wb") as f:
            f.write(response.content)
    else:
        return {"error": "Failed to download video from Cloudinary."}

    with ProcessPoolExecutor() as executor:
        future = executor.submit(check_video_for_sacrifice_animal, video_path)
        is_audhia = future.result()

    result = {"is_audhia": is_audhia}
    print(is_audhia)

    blurred_video_path = None  

    if is_audhia:
        donor_name = f"{req.first_name} {req.last_name}"
        mention_result = detect_donor_name(video_path, donor_name.strip())
        result.update(mention_result)
        print(mention_result)

        blurred_video_path = blur(video_path)
        print(blurred_video_path)

    print("uploading video...")

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )

    if blurred_video_path and os.path.exists(blurred_video_path):  
        blur_video = cloudinary.uploader.upload(
            blurred_video_path,
            asset_folder="blurred",
            public_id=f"blurred/{public_id}",
            overwrite=True,
            resource_type="video",
            format="mp4", 
        )
        result.update({"blurred_video_url": blur_video["url"]})
    else:
        result.update({"blurred_video_url": ""})

    return result

