# Video Searcher backend
This is a backend for a video searcher application.

It supports the following features:
- Upload videos, via a POST request
- Search for videos, via a GET request, by searching for the video frames label / subtitles
- Video processing, via a cronjob (temporarily disabled) - is available by running the `make process_video_frames` command

## Installation
To install the application, you need to have the following dependencies installed:
- Docker
- Docker Compose
- Make

## Running the application
To run the application, run the following command:
```bash
make up
```

## How video frames labeling works
Once a video is uploaded via POST /upload request (using the frontend application), the video entry in the processing queue for the job `video_frames_labeler`

This job pulls a batch of x videos (default 10) from the video collection, with processed field `false`, and processes them by doing the following algorithm:
- Extract the video frames, using the `ffmpeg` library. The frames are saved in the `frames` collection and in the assets folder, grouped by video_id. Each video is splitted into frames, with a 1 second window.
- The frames are labeled using the `resnet50` model, which is a pre-trained model for image classification. The labels are saved in the frame entry. I'm using a small sample of open sourced labels.
- For each frame, extract any visible text using the `tesseract` library. The extracted text is cleaned and splitted into lines, saved in each frame entry.
- The frames are saved in mongo collection.
- The video is processed, and the processed field is set to `true`.

To process the newly uploaded videos, run the following command
```bash
make process_video_frames
```

## API
The API is available at `http://localhost:8000`

## Known issues
- Video processing can be slow for bigger files. One improvement can be parallelizing the video processing job.
- The video processing job is not running automatically, you need to run the `make process_video_frames` command to process the videos
- No file limit for video uploads
- No proper validation on backend
- No proper error handling on backend
- No proper logging on backend
- No proper testing on backend
