"use client";

import { useState } from "react";
import { videoProcessorApi } from "@/api/VideoProcessorApi";

export default function SearchComponent() {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<SearchFoundVideo[]>([]);

  const handleSearch = async () => {
    console.log("Searching for:", query);
    try {
      const foundVideos = await videoProcessorApi.searchFrames(query);
      setResults(foundVideos);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <input
        type="text"
        className="p-2 border border-gray-300 rounded w-max"
        placeholder="Search videos"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        onClick={handleSearch}
        className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-2 px-4 rounded"
      >
        Search
      </button>
      <div className="flex flex-col items-center space-y-4">
        {results.map((video) => (
          <div key={video.id} className="flex flex-col items-center space-y-2">
            <h2 className="text-lg font-bold">{video.title}</h2>
            {video.matching_frames.map((frame) => (
              <div>
                <span className="text-sm font-semibold">
                  Frame {frame.timestamp}
                </span>
                <img
                  key={frame.id}
                  src={videoProcessorApi.getFrameAssetUrl(
                    video.id,
                    frame.filename,
                  )}
                  alt="frame"
                  className="w-64 h-36 object-cover"
                />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
