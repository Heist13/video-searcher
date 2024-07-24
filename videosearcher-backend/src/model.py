from typing import Optional

from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class Video(BaseModel):
    id: Optional[ObjectIdField] = None
    title: str
    filename: str
    processed: bool


class VideoFrame(BaseModel):
    id: Optional[ObjectIdField] = None
    video_id: ObjectIdField
    timestamp: int
    filename: str
    label: str
    text_lines: list[str]
