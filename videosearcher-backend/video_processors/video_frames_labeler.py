import argparse
import asyncio
import os
from typing import Dict, Any

import cv2
import requests
import torch
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from moviepy.editor import VideoFileClip
from torchvision import models, transforms
from PIL import Image
import pytesseract

from src.model import VideoFrame

load_dotenv()

# MongoDB setup
if "MONGO_CONNECTION_URI" not in os.environ:
    raise ValueError("MONGO_CONNECTION_URI environment variable is not set")

client = AsyncIOMotorClient(os.environ["MONGO_CONNECTION_URI"])
db = client.videoMetadataDb
videos_collection = db.videos
frames_collection = db.frames

FRAMES_DIR = "../assets/frames/"

# Load pre-trained model and set to evaluation mode
model = models.resnet50(pretrained=True)
model.eval()

# Define image transformations
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

# Load labels for the model
labels = requests.get("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt").text.split("\n")


def write_frame_on_disk(frame, video_id, timestamp) -> str:
    frame_name = f"{video_id}_{timestamp}.jpg"
    frame_path = f"{FRAMES_DIR}/{video_id}/{frame_name}"
    os.makedirs(os.path.dirname(frame_path), exist_ok=True)
    cv2.imwrite(frame_path, frame)

    return frame_name


def extract_text_lines_from_frame(frame):
    image = Image.fromarray(frame)
    text = pytesseract.image_to_string(image)
    lines = [line.lower() for line in text.split("\n") if line]
    cleaned_lines = []
    for line in lines:
        cleaned_line = " ".join([token for token in line.split() if token.isalnum()])
        cleaned_lines.append(cleaned_line)

    return cleaned_lines


def label_frame(frame):
    input_tensor = preprocess(frame)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top_prob, top_catid = torch.topk(probabilities, 1)

    return labels[top_catid[0]]


async def process_video(video: Dict[str, Any]):
    video_id = video["_id"]
    video_path = f"../assets/videos/{video['filename']}"

    clip = VideoFileClip(video_path)
    duration = clip.duration
    frame_docs = []
    for timestamp in range(0, int(duration), 1):
        frame = clip.get_frame(timestamp)
        frame_name = write_frame_on_disk(frame, video_id, timestamp)

        label = label_frame(frame)
        text_lines = extract_text_lines_from_frame(frame)

        frame_docs.append(VideoFrame(
            video_id=video_id,
            timestamp=timestamp,
            filename=frame_name,
            label=label,
            text_lines=text_lines
        ).dict())

    await frames_collection.insert_many(frame_docs)
    await videos_collection.update_one({"_id": video_id}, {"$set": {"processed": True}})


async def process_videos(batch_size: int):
    async for video in videos_collection.find({"processed": False}).limit(batch_size):
        await process_video(video)
        print(f"Processed video: {video['_id']} - {video['title']}")

    print("Processing complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process unprocessed videos and label frames.")
    parser.add_argument('--batch-size', type=int, default=10, help='Number of videos to process in each batch')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_videos(args.batch_size))
