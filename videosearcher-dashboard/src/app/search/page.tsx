import SearchComponent from "@/components/video-searcher/VideoSearchForm";

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold text-center mb-8">
        Search frames in the uploaded videos
      </h1>
      <SearchComponent />
    </main>
  );
}
