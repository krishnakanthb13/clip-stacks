# Social Media Announcements - Clip Stacks 🎬

## [v0.0.14] - 2026-03-26

### Platform 1: LinkedIn

Excited to announce the release of v0.0.14 of Clip Stacks 🎬!

Working with long-form video used to mean endless scrubbing or slow re-encoding to extract highlights. Clip Stacks changes that by letting you stream exact segments from your videos using mpv — no new files, no re-encoding, just pure streaming.

Since v0.0.1, we've come a long way:
🚀 Full GUI editor with H:M:S spinbox precision.
⚡ Smart Sync: Auto-detects video duration and formats timestamps for you.
🏗️ Robust Launchers: Support for Windows, macOS, and Linux with smart Python detection.
💾 Atomic Saves: Your profile data is now corruption-proof.

Whether you're reviewing lecture highlights or saving game clips, Clip Stacks keeps it lightweight and lightning-fast.

Check out the repo here: https://github.com/krishnakanthb13/clip-stacks

#OpenSource #VideoEditing #Python #Automation #DevUpdate #mpv

---

### Platform 2: Reddit

**Title:** [Show Reddit] Clip Stacks: Stream video highlights without re-encoding (v0.0.14 release)

Clip Stacks is a Python-based tool I've been building since v0.0.1 to solve a simple problem: extracting video segments without the overhead of video editing software or the wait for ffmpeg re-encoding.

**How it works:**
It uses `mpv`'s native seek flags (`--start` and `--end`) to play back a sequence of segments from different files as a single continuous "playlist."

**What's new in v0.0.14:**
*   **Precision GUI**: No more manual typing (though CLI is still there!); we now have discrete H:M:S spinboxes for frame-perfect control.
*   **Smart Sync**: It scans your video (via ffprobe) and automatically fills in the start/end times.
*   **Segment Editing**: You can now edit and update your highlights in-place.
*   **Resilient Launchers**: Improved error trapping to make sure it runs on any system with Python + mpv.

**Tech Stack:**
*   Python 3.8+ (Tkinter for GUI)
*   mpv player (the backbone)
*   JSON for portable profile storage

I'd love to hear your feedback or see how you might use it for your own video workflows!

**GitHub:** [krishnakanthb13/clip-stacks](https://github.com/krishnakanthb13/clip-stacks)

---

### Platform 3: X (Twitter)

Clip Stacks v0.0.14 is here! 🎬✨

Stream video highlights instantly without re-encoding. No new files, just pure playback via mpv.

✅ Precision H:M:S GUI
✅ Smart Video Sync
✅ Cross-platform launchers
✅ 100% Open Source (GPL v3)

Check it out: https://github.com/krishnakanthb13/clip-stacks

#OpenSource #Python #Video #DevLog
