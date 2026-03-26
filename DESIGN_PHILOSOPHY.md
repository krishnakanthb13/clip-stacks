# Design Philosophy 🏛️

Project: `clip-stacks`
Goal: Stream video highlights without re-encoding.

---

## 1. Problem Definition

Reviewing specific video clips (e.g. exercise form, workout highlights) often requires:
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

-   **Athletes**: Review squat form cues before a heavy set.
-   **Video Editors**: Quickly preview a set of raw clips for a rough cut.
-   **Teachers/Presenters**: Play specific highlights from long lectures.

---

## 5. Real-World Workflow Fit

1.  **Recording**: You record your workout sets.
2.  **Highlighting**: You open `clip-stacks` and mark the 25-second "work set" from a 3-minute video.
3.  **Reviewing**: Before your next workout, you hit "Play Profile" to see only your best reps.

---

## 6. Trade-offs & Constraints

### Subprocess Chaining
-   **Limitation**: Each segment is a separate `mpv` process.
-   **Constraint**: There's a 0.5s flicker between clips as one process closes and the next opens. This is an intentional trade-off for simplicity over a complex Libmpv integration.

### Playback Control
-   **Constraint**: You skip *segments* using `q`, and quit the *entire app* using `Q`. This overrides standard mpv quit behavior to provide a fluid multi-segment experience.
