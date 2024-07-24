"use client";

import React, { FormEvent, useState } from "react";
import { videoProcessorApi } from "@/api/VideoProcessorApi";
import { AxiosError } from "axios";

const isValidVideo = (file: File): boolean => {
  const validTypes = ["video/mp4", "video/quicktime", "video/x-msvideo"];
  return validTypes.includes(file.type);
};

const validateInput = (title: string, video: File | null): string[] => {
  const errors = [];
  if (!video) {
    errors.push("Please select a video file.");
  }
  if (video && !isValidVideo(video)) {
    errors.push("Invalid video file type. Supported types: mp4, mov, avi.");
  }

  if (!title || title.trim() === "") {
    errors.push("Please enter a title.");
  }

  return errors;
};

export default function VideoUploadForm(): React.JSX.Element {
  const [video, setVideo] = useState<File | null>(null);
  const [title, setTitle] = useState<string>("");
  const [errors, setErrors] = useState<string[]>([]);
  const [success, setSuccess] = useState<boolean>(false);

  const handleVideoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) {
      setVideo(null);
      return;
    }
    setVideo(files[0]);
  };

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSuccess(false);

    const submissionErrors = validateInput(title, video);
    if (submissionErrors.length > 0) {
      setErrors(submissionErrors);
      return;
    }

    const formData = new FormData();
    formData.append("video", video!);
    formData.append("title", title);

    if (submissionErrors.length > 0) {
      setErrors(submissionErrors);
      return;
    }

    try {
      await videoProcessorApi.uploadVideo(formData);
      setErrors([]);
      setSuccess(true);
    } catch (err) {
      if ((err as AxiosError).response?.status === 400) {
        setErrors([
          // @ts-ignore
          (err as AxiosError)?.response?.data?.message ??
            "Failed to upload video. Please try again.",
        ]);
        return;
      }

      console.error(err);
      setErrors(["Failed to upload video. Please try again."]);
    }
  };

  return (
    <div className="max-w-md bg-white p-16 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">Upload Video</h2>
      <form onSubmit={onSubmit}>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="title"
          >
            Video title
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter the video title"
            required
          />
        </div>
        <div className="mb-6">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="video"
          >
            File
          </label>
          <input
            type="file"
            id="video"
            onChange={handleVideoChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-800"
            required
          />
        </div>
        <div className="text-center">
          <button
            type="submit"
            className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-2 px-4 rounded"
          >
            Upload
          </button>
        </div>
        {errors.length > 0 &&
          errors.map((error) => (
            <p key={error} className="mt-4 text-center text-red-500">
              {error}
            </p>
          ))}
        {success && (
          <p className="mt-4 text-center text-green-500">
            Video uploaded successfully!
          </p>
        )}
      </form>
    </div>
  );
}
