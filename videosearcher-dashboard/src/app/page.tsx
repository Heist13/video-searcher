import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold text-center">
        Welcome to the Video Uploader
      </h1>
      <nav className="flex space-x-4">
        <Link href="/upload">
          <span className="text-2xl font-semibold text-blue-600 hover:text-blue-800 cursor-pointer">
            Upload
          </span>
        </Link>
        <Link href="/search">
          <span className="text-2xl font-semibold text-blue-600 hover:text-blue-800 cursor-pointer">
            Search
          </span>
        </Link>
      </nav>
    </main>
  );
}
