# Design Philosophy 🏛️

Project: `clip-stacks`
Goal: Stream video highlights without re-encoding.

---

## 1. Problem Definition

Reviewing specific video clips (e.g. lecture notes, game highlights, or raw footage) often requires:
1.  Opening a long video file.
2.  Scrubbing to find the right timestamp.
3.  Closing and finding the next clip.
4.  Alternatively, creating a new video file through slow, quality-degrading re-encoding.

`clip-stacks` solves this by automating the *seek-and-stop* feature of modern video players.

---

## 2. Why This Solution?

1.  **Speed**: No re-encoding means instant "highlights" as soon as you define the timestamps.
2.  **No Disk Bloat**: You don't need to save 5 versions of the same video just for different clips.
3.  **Cross-File Playlists**: You can mix segments from different files into a single "profile".
4.  **Smart Sync**: Automatically fetching durations via `ffprobe`/`mpv` removes the manual work of entering timestamps.
5.  **Aesthetics**: The modern GUI ensures a visually-pleasing experience that is as powerful as it is clean.

---

## 3. Design Principles

### Simplicity First
-   **No Database**: Plain JSON files are easy to backup and manually edit.
-   **Minimal Dependencies**: Only Python and `mpv`.

### Performance & Quality
-   **Zero Quality Loss**: The player seeks directly into the source file.
-   **No Temp Files**: Nothing is written to disk during playback.

### Precision & Control
- **H:M:S Discrete Input**: Trading complex string-writing for discrete spinboxes ensures users always input valid times with zero syntax errors.
- **Iterative Refinement**: Highlighting is an art. Users can now "Edit" segments to fine-tune start/end points without deleting and re-adding.

### Resilience
- **Data Integrity (Atomic Writes)**: Profiles are saved using `.tmp` buffers + `os.replace` to ensure zero corruption if the system crashes or power fails during a save.
- **Normalization & Fault Tolerance**: `load_profile` now validates every segment, auto-fixing missing labels and skipping invalid data. If your profile is slightly corrupted, the app cleans it up rather than crashing.
- **Global Error Trapping**: No silent failures — any startup crash is intercepted and reported with a detailed traceback.
- **Clean Process Management**: Support scripts specifically track the app process to ensure that interrupted runs clean up all resources (like the Python interpreter) gracefully.

### Flexibility
-   **GUI + CLI**: Professionals can script with the CLI; casual users can browse with the GUI.

---

## 4. Target Audience & Use Cases

-   **Students**: Review specific segments from long recorded lectures.
-   **Gamers**: Showcase high-skill moments from a long session.
-   **Video Editors**: Quickly preview a set of raw clips for a rough cut.

---

## 5. Real-World Workflow Fit

1.  **Recording**: You record or download a long video.
2.  **Highlighting**: You open `clip-stacks` and mark key timestamps (e.g. a 20-second explanation).
3.  **Reviewing**: When you need to study or showcase, you hit **▶ Play All** to see only the vital parts.

---

## 6. Trade-offs & Constraints

### Subprocess Chaining
-   **Limitation**: Each segment is a separate `mpv` process.
-   **Constraint**: There's a 0.5s flicker between clips as one process closes and the next opens. This is an intentional trade-off for simplicity over a complex Libmpv integration.

### Playback Control
-   **Constraint**: You skip *segments* using `q`, and quit the *entire app* using `Q`. Both **▶ Play All** and **▶ Play from Selected** trigger a background `mpv` queue; this overrides standard `mpv` quit behavior to provide a fluid multi-segment experience.

### Choosing `mpv` + `ffprobe`
- Leveraging `mpv`'s command-line interface instead of native bindings results in simpler code and easier cross-platform distribution.
- If `ffprobe` is present, we use it for faster, near-instant duration extraction; otherwise, `mpv` is used as a reliable fallback.
