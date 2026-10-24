# yt-download

YouTube MP4 (highest resolution) and MP3 (320kbps) downloader powered by `uv` and `yt-dlp`—usable as a CLI, Tkinter GUI, or AI Agent Skill.

## Usage with `uv`

```bash
# Download highest-resolution MP4 to ~/Downloads
uv run youtube_video_indir.py "<youtube_url>"

# Download 320kbps MP3 to ~/Downloads
uv run youtube_video_indir.py "<youtube_url>" --format mp3

# Launch Tkinter GUI
uv run youtube_video_indir.py
```

## Agent Skill

The skill lives in [`.agents/skills/youtube-downloader/SKILL.md`](.agents/skills/youtube-downloader/SKILL.md) and uses the standalone PEP 723 script [`.agents/skills/youtube-downloader/scripts/download.py`](.agents/skills/youtube-downloader/scripts/download.py).
