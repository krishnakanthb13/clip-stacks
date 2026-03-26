<p align="center">
  <img src="assets/logo.png" width="160" height="160" alt="Clip Stacks Logo" />
</p>

<h1 align="center">Clip Stacks 🎬💪</h1>

<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0">
    <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3" />
  </a>
</p>

<p align="center">
  <strong>Stream video highlights. No re-encoding. No new files. Just your clips.</strong>
</p>

Clip Stacks lets you define timestamp-based highlight playlists across multiple video files — and play them back instantly using `mpv`. Perfect for reviewing specific segments from lectures, game highlights, or any long-form video.

---

- ✅ **Precision H:M:S Controls** — Discrete spinboxes for hours, minutes, and seconds.
- ✅ **Segment Editing** — Update existing highlights without re-adding them.
- ✅ **Smart Time Sync** — Auto-detects video duration and pre-fills timestamps.
- ✅ **No new video files created** — pure streaming via seek.
- ✅ **Multiple profiles** — categorize highlights by type.
- ✅ **Cross-platform** — Windows, macOS, Linux.
- ✅ **Modern GUI** — Clean interface with hover effects and live stats.
- ✅ **Minimalist dependencies** — just Python 3.8+ and `mpv`.
- ✅ **Robust Launchers** — Smart Python detection (`py`, `python`, `python3`), existence checks, and specific process cleanup.
- ✅ **Atomic Saves** — Uses temporary files to prevent profile corruption during crashes.
- ✅ **Fault-Tolerant Loading** — Automatically validates and normalizes segments; skips invalid data with warnings.
- ✅ **GPL v3 licensed** — fork it, improve it, own it.

---

## Installation

### 1. Install mpv (the only real dependency)

| Platform | Command |
|----------|---------|
| **macOS** | `brew install mpv` |
| **Ubuntu/Debian** | `sudo apt install mpv` |
| **Arch** | `sudo pacman -S mpv` |
| **Windows** | Download from [mpv.io](https://mpv.io/installation/) and add to PATH |

### 2. Install Clip Stacks

```bash
# Clone the repo
git clone https://github.com/krishnakanthb13/clip-stacks.git
cd clip-stacks

# No pip install needed — just run it
python clip-stacks.py --gui        # graphical editor
python clip-stacks.py list         # CLI mode
```

> **Optional:** `pip install python-mpv` for future embedded playback support (not required for current version).

---

## Quick Start

### Easy Launch 🚀

If you are on Windows, simply double-click:
- **`launch_clip_stacks.bat`**

If you are on macOS/Linux, run:
- **`bash launch_clip_stacks.sh`**

---

### GUI (Manual)

```bash
python clip-stacks.py --gui
```

1. Click **+ New** → name your profile (e.g. `MovieHighlights`)
2. In the "Add Segment" form → click **📁 Browse** for your video file.
3. **Timestamp Entry**: Use the discrete **H:M:S spinboxes** for precise control.
4. **Smart Sync**: Clip Stacks will automatically fetch the video duration and fill in the `Start` (`0:00:00`) and `End` times for you.
5. (Optional) Adjust timestamps or add a `Label` like `"Cool chase scene"`.
6. Click **+ Add Segment**.
7. **Refine**: Need a change? Select a segment and click **✎ Edit** to load it back into the form.
8. **💾 Save** → **▶ Play All** (starts from segment 1) or **▶ Play From Selected** (starts from your current selection).
9. **Auto-save**: The app automatically saves your profile before playback starts to ensure your latest changes are active.

> [!TIP]
> You can also use the **⟳ Sync** button at any time to reset the timestamps to the full video duration. The launcher now supports UTF-8 (chcp 65001) for better emoji and path rendering on Windows.

### CLI

```bash
# Create a profile
python clip-stacks.py new Highlights "General highlights"

# Add segments from different video files
python clip-stacks.py add Highlights ~/videos/clip1.mp4  1:22  3:35  "Key segment 1"
python clip-stacks.py add Highlights ~/videos/clip2.mp4  0:45  2:10  "Key segment 2"
python clip-stacks.py add Highlights ~/videos/clip3.mp4  5:00  7:30  "Key segment 3"

# Show what's in it
python clip-stacks.py show Highlights

# Play it
python clip-stacks.py play Highlights

# Edit a segment (index 2)
python clip-stacks.py edit Highlights 2 video.mp4 1:00 2:30 "Updated label"

# Start from segment 3
python clip-stacks.py play Highlights --from 3

# List all profiles
python clip-stacks.py list
```

---

## Profile Format

Profiles are plain JSON files stored in `~/.clip-stacks/profiles/`. You can edit them by hand:

```json
{
  "name": "Highlights",
  "description": "Important video marks",
  "segments": [
    {
      "video": "/home/user/videos/movie.mp4",
      "start": 82.0,
      "end": 215.0,
      "label": "Cool scene"
    },
    {
      "video": "/home/user/videos/lecture.mp4",
      "start": 45.0,
      "end": 130.0,
      "label": "Key definition"
    }
  ]
}
```

---

## How It Works

Clip Stacks uses `mpv`'s native `--start` and `--end` flags to seek into a video and stop at a precise timestamp — **no re-encoding, no temp files**. Each segment is a separate mpv subprocess; they chain automatically.

```
mpv video.mp4 --start=82 --end=215
mpv other.mp4 --start=45 --end=130
...
```

---

## Keyboard Shortcuts (during playback)

| Key | Action |
|-----|--------|
| `q` | Skip to next segment |
| `Q` | Quit Clip Stacks entirely |
| `Space` | Pause / Resume |
| `←` / `→` | Seek ±5 seconds |
| `f` | Toggle fullscreen |

(All standard `mpv` keyboard shortcuts work as expected.)

---

## 🛠️ Requirements & Troubleshooting

### Requirements
- **Python 3.8+**
- **mpv player**: The backbone of the playback engine.
- **ffprobe** (optional): Greatly speeds up video duration detection. Usually comes bundled with `ffmpeg`.

### Common Issues
- **`mpv not found`**: Ensure `mpv` (or `mpv.exe` on Windows) is in your system `PATH`.
- **GUI fails to open**: Ensure `tkinter` is installed. On some Linux distros, you may need `sudo apt install python3-tk`.
- **App opens and closes immediately**: The launcher now includes a **Global Error Trap** and an **Entry Existence Check**. If the script is missing or a crash occurs, you will receive a clear diagnostic message.
- **Improved Cleanup**: Closing the launcher (Ctrl+C) now specifically targets the app process, ensuring a clean exit without orphaned `mpv` windows.

---

## Roadmap / Ideas

- [ ] Drag-and-drop video files into GUI
- [ ] Preview thumbnail on hover
- [ ] Export profile as `.m3u8` for VLC
- [ ] Import timestamps from YouTube chapter format
- [ ] Total duration estimate per profile

---

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for our feature request and pull request workflow.

---

## 📚 Documentation

Detailed documentation is available in the repository:

*   [**Design Philosophy**](DESIGN_PHILOSOPHY.md) — The "Why" and "How" behind the project.
*   [**Code Documentation**](CODE_DOCUMENTATION.md) — Deep dive into the architecture and data flows.
*   [**Contributing Guide**](CONTRIBUTING.md) — How to report bugs and suggest features.

---

## License

GPL v3 — see [LICENSE](LICENSE) for details.
