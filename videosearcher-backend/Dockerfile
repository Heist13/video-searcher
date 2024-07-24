# Use an official Python runtime as a parent image
FROM arm64v8/python:3.12-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg

ENV PYTHONPATH=/app

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
