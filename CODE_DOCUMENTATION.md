# Clip Stacks Code Documentation 🛠️

Project: `clip-stacks`
Goal: Stream video highlights using `mpv` timestamps without re-encoding.

---

## 1. Project Structure

| File / Folder | Purpose |
| :--- | :--- |
| `clip-stacks.py` | Main application script (logic + GUI + CLI). |
| `launch_clip_stacks.bat` | Windows launcher (runs python + `--gui`). |
| `launch_clip_stacks.sh` | Unix launcher (runs python3 + `--gui`). |
| `README.md` | General overview and usage guide. |
| `LICENSE` | GPL v3 license text. |
| `CODE_DOCUMENTATION.md` | Deep dive into codebase (this file). |
| `DESIGN_PHILOSOPHY.md` | Rationale and core principles. |
| `CONTRIBUTING.md` | Guide for community contributions. |

---

## 2. High-Level Architecture

`clip-stacks` is a standalone Python application that acts as a wrapper around the `mpv` player.

1.  **Data Layer**: JSON-based profiles stored in `~/.clip-stacks/profiles/`.
2.  **Core Logic**: Functions to parse timestamps, load/save profiles, and manage segments.
3.  **Playback Engine**: Subprocess-based execution of `mpv` with specific start/end flags.
4.  **Interface Layer**: Two-mode interface:
    -   **CLI**: Using `argparse` for rapid segment management and playback.
    -   **GUI**: Using `tkinter` for interactive editing and profile browsing.

---

## 3. Core Modules & Functions

### Profile Management
- `load_profile(name)`: Reads JSON from the filesystem.
- `save_profile(name, data)`: Persists profile as formatted JSON.
- `add_segment(profile, video, start, end, label)`: Validates and appends segments.

### Help & Utils
- `parse_time(t)`: Converts `H:MM:SS` or `MM:SS` strings to float seconds.
- `fmt_time(s)`: Converts float seconds back to readable `H:MM:SS`.
- `find_mpv()`: Locates `mpv` executable across different systems and PATHs.

### Playback Engine
- `play_profile(profile, start_index)`: Iterates through segments and spawns `mpv` processes sequentially.

---

## 4. Data Flow

```mermaid
graph TD
    User([User]) --> CLI[CLI Command]
    User --> GUI[Graphical UI]
    CLI --> Logic[Core Logic]
    GUI --> Logic
    Logic <--> Files[(JSON Profiles)]
    Logic --> Engine[Playback Engine]
    Engine --> MPV[mpv Subprocess]
    MPV --> Output[Video Stream]
```

---

## 5. Dependencies

### Runtime
- **Python 3.8+**: Language runtime.
- **mpv**: Required for video playback. Must be in system `PATH`.

### Optional
- **tkinter**: Required for the `--gui` mode (standard on most Python installs).
- **python-mpv**: (Placeholder) Hook for future embedded playback support.

---

## 6. Execution Flow

1.  **Entry Point**: `cli_main()` parses arguments.
2.  **Mode Switch**:
    -   If `--gui` or no command: `gui_main()` launches `ClipStacksApp`.
    -   Else: Routes to CLI sub-command handlers (`p_play`, `p_add`, etc.).
3.  **IO**: File data is loaded from `Path.home() / ".clip-stacks" / "profiles"`.
4.  **Playback**: Each segment triggers a synchronous `subprocess.run([mpv, ...])` call.
5.  **Termination**: `mpv` exit codes are monitored (e.g. `4` for user-quit).
