import VideoUploadForm from "@/components/video-uploader/VideoUploadForm";

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold text-center mb-8">Upload Your Video</h1>
      <VideoUploadForm />
    </main>
  );
}
