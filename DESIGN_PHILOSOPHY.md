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
4.  **Minimalist Stack**: Relies on `mpv` — a powerful, standard, and portable player.

---

## 3. Design Principles

### Simplicity First
-   **No Database**: Plain JSON files are easy to backup and manually edit.
-   **Minimal Dependencies**: Only Python and `mpv`.

### Performance & Quality
-   **Zero Quality Loss**: The player seeks directly into the source file.
-   **No Temp Files**: Nothing is written to disk during playback.

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
3.  **Reviewing**: When you need to study or showcase, you hit "Play Profile" to see only the vital parts.

---

## 6. Trade-offs & Constraints

### Subprocess Chaining
-   **Limitation**: Each segment is a separate `mpv` process.
-   **Constraint**: There's a 0.5s flicker between clips as one process closes and the next opens. This is an intentional trade-off for simplicity over a complex Libmpv integration.

### Playback Control
-   **Constraint**: You skip *segments* using `q`, and quit the *entire app* using `Q`. This overrides standard mpv quit behavior to provide a fluid multi-segment experience.
