import axios, { AxiosInstance } from "axios";

class VideoProcessorApi {
  protected readonly baseUrl: string;
  protected readonly apiClient: AxiosInstance;

  public constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || "";
    this.apiClient = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL,
    });
  }

  public async uploadVideo(formData: FormData): Promise<void> {
    try {
      await this.apiClient.post("/upload", formData);
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  public async searchFrames(query: string): Promise<SearchFoundVideo[]> {
    try {
      const { data } = await this.apiClient.get<SearchFoundVideo[]>(
        `/search?query=${query}`,
      );
      return data;
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  public getFrameAssetUrl(videoId: string, frameFilename: string): string {
    return `${this.baseUrl}/${videoId}/frames/${frameFilename}`;
  }
}

export const videoProcessorApi = new VideoProcessorApi();
