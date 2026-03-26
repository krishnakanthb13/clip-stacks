# Release Notes - Clip Stacks 🎬

## [v0.0.14] - 2026-03-26

**The Resilience & Polish Update.** This release focuses on final refinements to the UI and documentation, ensuring a smooth experience for new users.

### 🚀 New Features
- **Smart Video Sync**: Automatic detection of video duration via `ffprobe`, pre-populating segment time fields.
- **Segment Editing**: Full support for updating existing highlights directly in the GUI and CLI.
- **Precision Time Controls**: Discrete H:M:S spinboxes for frame-perfect highlight selection.

### ⚡ Improvements
- **Robust Launching**: Re-engineered launchers (`.bat` and `.sh`) with global error traps, smart Python detection, and process existence checks.
- **Atomic Saves**: Profile data is now saved using temporary files to prevent corruption during unexpected shutdowns.
- **Modernized UI**: Refined layout with hover effects, status badges, and improved accessibility labels.

### 🐛 Bug Fixes
- Fixed process leak where closing the launcher left orphaned `mpv` windows.
- Resolved profile loading errors by implementing stricter JSON validation and normalization.
- Improved Windows terminal compatibility with UTF-8 support (chcp 65001).

### 📚 Documentation
- Comprehensive README update with installation tables and troubleshooting guides.
- New `DESIGN_PHILOSOPHY.md` and `CODE_DOCUMENTATION.md` for maintainers.

---

## [v0.0.10] - 2026-03-24
### 🏗️ Infrastructure & Maintenance
- Modularized the GUI builder for better maintainability.
- Enhanced Python detection logic to prefer `py` on Windows if multiple versions are installed.

---

## [v0.0.5] - 2026-03-21
### 🚀 New Features
- **Initial GUI Implementation**: The first graphical editor for Clip Stacks goes live.
- **CLI Basic Mode**: Support for `list`, `show`, and `play` commands.

---

## [v0.0.1] - 2026-03-17
### 🚀 New Features
- **Core Engine**: Initial release of the `mpv`-based streaming engine (no re-encoding!).
- **JSON Profile System**: Portable, human-readable highlight storage.
