from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.model import Video, VideoFrame
from src.object_storage import ObjectStorage


class VideoSearcher():
    def __init__(self, videos_collection: AsyncIOMotorCollection, frames_collection: AsyncIOMotorCollection,
                 object_storage: ObjectStorage):
        self._videos_collection = videos_collection
        self._frames_collection = frames_collection
        self._object_storage = object_storage

    async def search_videos(self, query: str) -> (list[Video], list[VideoFrame]):
        cursor = self._frames_collection.find(self._filter_query_match(query))
        found_frames = []
        async for document in cursor:
            found_frames.append(VideoFrame(
                id=document["_id"],
                video_id=document["video_id"],
                timestamp=document["timestamp"],
                filename=document["filename"],
                label=document["label"],
                text_lines=document["text_lines"]
            ))

        videos = self._videos_collection.find({"_id": {"$in": [frame.video_id for frame in found_frames]}})
        videos = [Video(
            id=video["_id"],
            title=video["title"],
            filename=video["filename"],
            processed=video["processed"]
        ) async for video in videos]

        print(videos, found_frames)

        return videos, found_frames

    async def search_in_video(self, video_id: str, query: str) -> list[VideoFrame]:
        cursor = self._frames_collection.find({
            "video_id": ObjectId(video_id),
        } | self._filter_query_match(query))
        found_frames = []
        async for document in cursor:
            found_frames.append(VideoFrame(**document))

        return found_frames

    def _filter_query_match(self, query: str) -> dict[str, Any]:
        return {
            "$or": [
                {"label": {"$regex": query, "$options": "i"}},
                {"text_lines": {"$elemMatch": {"$regex": query, "$options": "i"}}}
            ]
        }