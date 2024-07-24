from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorCollection

from src.model import Video
from src.object_storage import ObjectStorage


class VideoUploader:

    def __init__(self, videos_collection: AsyncIOMotorCollection, object_storage: ObjectStorage, video_dir: str):
        self._videos_collection = videos_collection
        self._video_dir = video_dir
        self._object_storage = object_storage

    async def upload_video(self, title: str, video: UploadFile):
        video_filename = self._object_storage.upload(video.file, video.filename, self._video_dir)

        doc = Video(
            title=title,
            filename=video_filename,
            processed=False
        ).dict()
        await self._videos_collection.insert_one(doc)
