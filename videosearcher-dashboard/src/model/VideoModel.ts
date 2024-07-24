interface Frame {
  id: string;
  timestamp: number;
  filename: string;
  label: string;
  text_lines: string[];
}

interface Video {
  id: string;
  title: string;
  filename: string;
}

interface SearchFoundVideo {
  id: string;
  title: string;
  filename: string;
  matching_frames: Frame[];
}
