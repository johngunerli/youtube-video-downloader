---
name: youtube-downloader
description: Use when the user asks to download a YouTube video or audio track, convert a YouTube link to MP4 or MP3, or grab media from a YouTube URL.
---

# YouTube Downloader

## Overview

Downloads YouTube videos as highest-resolution **MP4** or **320kbps MP3** audio using `uv` and `yt-dlp` (with `ffmpeg` for audio extraction and stream merging).

The bundled script [scripts/download.py](./scripts/download.py) uses PEP 723 inline dependency metadata, so `uv run` automatically manages an isolated environment with `yt-dlp` without needing a pre-activated virtualenv or `requirements.txt`.

## Quick Reference

| Task | Command |
| :--- | :--- |
| **Download MP4 (default, to `~/Downloads`)** | `uv run <skill_dir>/scripts/download.py "<url>"` |
| **Download 320kbps MP3 (to `~/Downloads`)** | `uv run <skill_dir>/scripts/download.py "<url>" --format mp3` |
| **Download to current working directory** | `uv run <skill_dir>/scripts/download.py "<url>" --format mp4 --output-dir .` |
| **Download with custom filename** | `uv run <skill_dir>/scripts/download.py "<url>" --format mp4 --output-dir . --filename "video.%(ext)s"` |

## Workflow

1. **Determine format and destination**:
   - Default format is `mp4` (highest resolution MP4 + M4A merged). Use `--format mp3` when the user asks for audio, music, or MP3 (extracts 320kbps MP3 via `ffmpeg`).
   - Default output directory is `~/Downloads`. Override with `--output-dir <path>` if the user specifies where to save the file (e.g., Desktop or current workspace).
2. **Run the download script via `uv run`** (using the path to [scripts/download.py](./scripts/download.py) relative to this `SKILL.md` file):
   ```bash
   uv run <path-to-this-skill>/scripts/download.py "<youtube_url>" --format mp4 --output-dir ~/Downloads
   ```
3. **Verify output**:
   - Check the command output for `Title:` and `Saved to:` and confirm the resulting `.mp4` or `.mp3` file exists on disk before reporting completion.

## Prerequisites & Troubleshooting

- **`uv` and `ffmpeg` required**: `ffmpeg` must be on `PATH` (`/opt/homebrew/bin/ffmpeg` on macOS) for merging high-resolution video/audio streams and converting audio to 320kbps MP3. If missing, install via `brew install ffmpeg`.
- **Do not use `pytube` or `youtube_dl`**: Legacy libraries fail with HTTP 400 / cipher errors on current YouTube endpoints. Always use `yt-dlp` via `uv run`.
