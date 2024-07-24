import os
import shutil
import uuid
from collections import defaultdict

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

from src.object_storage import LocalStorage
from src.video_searcher import VideoSearcher
from src.video_uploader import VideoUploader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
if "MONGO_CONNECTION_URI" not in os.environ:
    raise ValueError("MONGO_CONNECTION_URI environment variable is not set")

print(os.environ["MONGO_CONNECTION_URI"])

client = AsyncIOMotorClient(os.environ["MONGO_CONNECTION_URI"])
db = client.videoMetadataDb
videos_collection = db.videos
frames_collection = db.frames

# Prep the videos directory
VIDEO_DIR = "./assets/videos/"
os.makedirs(VIDEO_DIR, exist_ok=True)

# Init services
local_storage = LocalStorage()
video_uploader = VideoUploader(videos_collection, local_storage, VIDEO_DIR)
video_searcher = VideoSearcher(videos_collection, frames_collection, local_storage)


# Request Schema
class VideoSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)


@app.post("/upload")
async def upload_video(title: str = Form(), video: UploadFile = File(...)):
    try:
        data = VideoSchema(title=title)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)

    try:
        await video_uploader.upload_video(data.title, video)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500)

    return JSONResponse(content={"message": "Video uploaded successfully"}, status_code=200)


@app.get("/search")
async def search_videos(query: str):
    videos, found_frames = await video_searcher.search_videos(query)
    frames_per_video = defaultdict(list)
    for frame in found_frames:
        frames_per_video[str(frame.video_id)].append({
            "id": str(frame.id),
            "timestamp": frame.timestamp,
            "filename": frame.filename,
            "label": frame.label,
            "text_lines": frame.text_lines
        })

    response = []
    for video in videos:
        response.append({
            "id": str(video.id),
            "title": video.title,
            "filename": video.filename,
            "matching_frames": frames_per_video[str(video.id)]
        })

    return JSONResponse(content=response, status_code=200)


@app.get("/{video_id}/frames/{frame_filename}")
async def show_frame(video_id: str, frame_filename: str):
    return FileResponse(f"./assets/frames/{video_id}/{frame_filename}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
