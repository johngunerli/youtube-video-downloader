#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "yt-dlp>=2024.10.0",
# ]
# ///
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yt_dlp


def download_video(link: str, output_dir: Path | str = Path.cwd()) -> Path:
    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        print("Title: ", info.get("title"))
        print("Number of views: ", info.get("view_count"))
        print("Length of video: ", info.get("duration"))
        final_path = Path(ydl.prepare_filename(info)).with_suffix(".mp4")
        print("Download completed!! ->", final_path)
        return final_path


def download_audio(link: str, output_dir: Path | str = Path.cwd()) -> Path:
    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        final_path = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
        print("Audio download completed!! ->", final_path)
        return final_path


def run_gui() -> None:
    import tkinter as tk
    from tkinter import Entry

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    root.geometry("400x400")
    root.title("Youtube Video İndirici")

    e = Entry(root, width=50)
    e.pack()
    e.focus_set()

    var = tk.StringVar()
    label = tk.Label(root, textvariable=var, relief=tk.RAISED)
    var.set("Linki gir, mp4 mu mp3 mu sec insin.")

    def mp4() -> None:
        download_video(e.get())
        var.set("Video indi!")

    def mp3() -> None:
        download_audio(e.get())
        var.set("Ses indi!")

    button = tk.Button(frame, text="mp4", command=mp4)
    button.pack(side=tk.LEFT)
    button2 = tk.Button(frame, text="mp3", command=mp3)
    button2.pack(side=tk.LEFT)

    label.pack()
    root.mainloop()


def main() -> int:
    if len(sys.argv) == 1:
        run_gui()
        return 0

    parser = argparse.ArgumentParser(
        description="YouTube MP4 / MP3 Downloader (CLI & GUI)"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-f",
        "--format",
        choices=["mp4", "mp3"],
        default="mp4",
        help="Download format: mp4 or mp3 (default: mp4)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=str(Path.home() / "Downloads"),
        help="Output directory (default: ~/Downloads)",
    )
    args = parser.parse_args()
    if args.format == "mp3":
        download_audio(args.url, args.output_dir)
    else:
        download_video(args.url, args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
