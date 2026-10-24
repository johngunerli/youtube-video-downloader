#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "yt-dlp>=2024.10.0",
# ]
# ///
"""CLI helper for the youtube-downloader skill."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yt_dlp


def download_media(
    url: str,
    fmt: str = "mp4",
    output_dir: Path | str = Path.home() / "Downloads",
    filename: str | None = None,
) -> Path:
    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    template_name = filename if filename else "%(title)s.%(ext)s"
    outtmpl = str(out_dir / template_name)

    if fmt == "mp3":
        ydl_opts: dict = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
        }
    else:
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "outtmpl": outtmpl,
            "noplaylist": True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        prepared = Path(ydl.prepare_filename(info))
        final_path = prepared.with_suffix(".mp3" if fmt == "mp3" else ".mp4")
        print(f"Title: {info.get('title')}")
        print(f"Number of views: {info.get('view_count')}")
        print(f"Length of video: {info.get('duration')}s")
        print(f"Saved to: {final_path}")
        return final_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download a YouTube video as highest-resolution MP4 or 320kbps MP3."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-f",
        "--format",
        choices=["mp4", "mp3"],
        default="mp4",
        help="Output format: mp4 (highest resolution video) or mp3 (320kbps audio). Default: mp4",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=str(Path.home() / "Downloads"),
        help="Directory to save the downloaded file (default: ~/Downloads)",
    )
    parser.add_argument(
        "-n",
        "--filename",
        default=None,
        help="Optional custom filename template (e.g. 'video.%%(ext)s')",
    )
    args = parser.parse_args()
    download_media(
        url=args.url,
        fmt=args.format,
        output_dir=args.output_dir,
        filename=args.filename,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
