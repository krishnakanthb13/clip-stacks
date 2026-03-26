# Contributing to Clip Stacks 🤝

Welcome! `clip-stacks` is designed to be minimal — the core logic is intentionally kept small (~100 lines for profiling, ~100 for playback).

## 1. Feature Suggestions & Bug Reporting

-   **Bugs**: Use GitHub Issues. Please include:
    -   Your OS.
    -   Your `mpv` version.
    -   The problematic profile's JSON content.
-   **Features**: We prioritize features that don't add heavy new dependencies.

## 2. Workflow: Fork -> Branch -> PR

1.  **Fork** the repo: `https://github.com/krishnakanthb13/clip-stacks`
2.  **Create** your feature branch: `git checkout -b feature/cool-new-idea`
3.  **Commit** your changes: `git commit -m 'Add support for Y'`
4.  **Push** to the branch: `git push origin feature/cool-new-idea`
5.  **Open** a Pull Request.

## 3. Local Development Setup

No special installation needed!

```bash
# Clone your fork
git clone https://github.com/your-username/clip-stacks.git
cd clip-stacks

# Run it directly
python clip-stacks.py --help
```

## 4. Pre-submission Checklist

Ensure your change:
-   [ ] Passes `python -m py_compile clip-stacks.py` (basic syntax check).
-   [ ] Doesn't break the CLI commands (test `new`, `add`, `list`, `play`).
-   [ ] Maintains the "Zero Quality Loss" principle (no re-encoding).
-   [ ] Keeps the code readable and minimalist.

## 5. Coding Style

-   Use standard PEP 8 where possible.
-   Keep comments clear but concise.
-   Avoid large external libraries if a standard Python lib or `mpv` flag works.

Thank you for contributing to better workout reviews! 💪🎬
