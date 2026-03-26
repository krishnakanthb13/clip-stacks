#!/usr/bin/env python3
"""
Clip Stacks 🎬💪
─────────────────────────────────────────────────────────────
Stream video highlights from multiple files using timestamps.
No re-encoding. No new files. Just your reps.

Author: Krishna Kanth B
License: GPL v3
Requires: mpv installed on your system
          pip install python-mpv  (optional, for embedded playback)
"""

import json
import os
import sys
import subprocess
import shutil
import argparse
import time
from pathlib import Path

# ── Optional tkinter GUI ──────────────────────────────────────────────────────
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, simpledialog
    HAS_TK = True
except ImportError:
    HAS_TK = False

PROFILES_DIR = Path.home() / ".clip-stacks" / "profiles"
PROFILES_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# Core: timestamp helpers
# ─────────────────────────────────────────────────────────────────────────────

def parse_time(t: str) -> float:
    """Accept 'HH:MM:SS', 'MM:SS', or raw seconds string → float seconds."""
    t = t.strip()
    parts = t.split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        else:
            return float(t)
    except ValueError:
        raise ValueError(f"Cannot parse timestamp: '{t}'  (use MM:SS or HH:MM:SS)")


def fmt_time(seconds: float) -> str:
    """Float seconds → 'H:MM:SS' string."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ─────────────────────────────────────────────────────────────────────────────
# Core: Profile I/O
# ─────────────────────────────────────────────────────────────────────────────

def profile_path(name: str) -> Path:
    return PROFILES_DIR / f"{name}.json"


def list_profiles() -> list[str]:
    return sorted(p.stem for p in PROFILES_DIR.glob("*.json"))


def load_profile(name: str) -> dict:
    p = profile_path(name)
    if not p.exists():
        raise FileNotFoundError(f"Profile '{name}' not found.")
    with open(p) as f:
        return json.load(f)


def save_profile(name: str, data: dict):
    with open(profile_path(name), "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅  Profile '{name}' saved → {profile_path(name)}")


def new_profile(name: str) -> dict:
    return {"name": name, "description": "", "segments": []}


def add_segment(profile: dict, video: str, start: str, end: str, label: str = ""):
    """Append a segment entry; validates timestamps."""
    s = parse_time(start)
    e = parse_time(end)
    if e <= s:
        raise ValueError(f"End ({end}) must be after start ({start})")
    profile["segments"].append({
        "video": os.path.abspath(video),
        "start": s,
        "end":   e,
        "label": label or f"{Path(video).stem}  {fmt_time(s)}–{fmt_time(e)}"
    })


# ─────────────────────────────────────────────────────────────────────────────
# Core: Playback engine (subprocess mpv — works everywhere)
# ─────────────────────────────────────────────────────────────────────────────

def find_mpv() -> str:
    """Return path to mpv binary or raise."""
    binary = "mpv.exe" if sys.platform == "win32" else "mpv"
    path = shutil.which(binary)
    if path:
        return path
    # Common fallback locations
    fallbacks = [
        r"C:\Program Files\mpv\mpv.exe",
        r"C:\Program Files (x86)\mpv\mpv.exe",
        "/usr/bin/mpv", "/usr/local/bin/mpv",
        "/opt/homebrew/bin/mpv",
    ]
    for fb in fallbacks:
        if os.path.isfile(fb):
            return fb
    raise FileNotFoundError(
        "mpv not found. Install it:\n"
        "  Windows : https://mpv.io/installation/\n"
        "  macOS   : brew install mpv\n"
        "  Linux   : sudo apt install mpv  (or your distro's package manager)"
    )


def play_profile(profile: dict, start_index: int = 0, verbose: bool = True):
    """
    Play each segment via mpv subprocess.
    mpv handles seeking natively — no re-encoding, no new files.
    """
    mpv = find_mpv()
    segments = profile["segments"]
    total = len(segments)

    if not segments:
        print("⚠️  Profile has no segments.")
        return

    print(f"\n🎬  Clip Stacks — {profile['name']}")
    if profile.get("description"):
        print(f"    {profile['description']}")
    print(f"    {total} segment(s)  •  playing from #{start_index + 1}\n")
    print("    Press  q  to skip to next segment")
    print("    Press  Q  to quit entirely\n")
    print("─" * 50)

    quit_all = False
    for i, seg in enumerate(segments[start_index:], start=start_index):
        if quit_all:
            break

        label = seg.get("label", "")
        dur   = seg["end"] - seg["start"]
        print(f"\n  [{i+1}/{total}]  {label}")
        print(f"           {seg['video']}")
        print(f"           {fmt_time(seg['start'])} → {fmt_time(seg['end'])}  ({fmt_time(dur)})")

        if not os.path.isfile(seg["video"]):
            print(f"  ⚠️  File not found, skipping.")
            continue

        cmd = [
            mpv,
            seg["video"],
            f"--start={seg['start']}",
            f"--end={seg['end']}",
            "--keep-open=no",          # auto-advance
            "--really-quiet",
            f"--title=Clip Stacks [{i+1}/{total}] {label}",
        ]

        try:
            result = subprocess.run(cmd)
            if result.returncode == 4:   # mpv exit code 4 = user pressed Q
                print("\n  ⏹  Quit by user.")
                quit_all = True
        except KeyboardInterrupt:
            print("\n  ⏹  Interrupted.")
            break
        except FileNotFoundError:
            print(f"\n  ❌  mpv binary not found at: {mpv}")
            break

    print("\n✅  Clip Stacks session complete.\n")


# ─────────────────────────────────────────────────────────────────────────────
# CLI interface
# ─────────────────────────────────────────────────────────────────────────────

def cli_main():
    parser = argparse.ArgumentParser(
        prog="clip-stacks",
        description="Clip Stacks 🎬💪 — play video highlights by timestamp, no re-encoding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  clip-stacks --gui                                # Open graphical editor
  clip-stacks list                                 # List saved profiles
  clip-stacks play  LegDay                         # Play a profile
  clip-stacks play  LegDay --from 3               # Start from segment #3
  clip-stacks new   LegDay "Leg day highlights"
  clip-stacks add   LegDay video.mp4 1:22 3:35 "Squat form"
  clip-stacks add   LegDay other.mp4 0:45 2:10
  clip-stacks show  LegDay
  clip-stacks delete LegDay
        """
    )

    parser.add_argument("--gui", action="store_true", help="Launch the graphical editor")
    sub = parser.add_subparsers(dest="cmd")

    # list
    sub.add_parser("list", help="List all profiles")

    # play
    p_play = sub.add_parser("play", help="Play a profile")
    p_play.add_argument("profile")
    p_play.add_argument("--from", dest="from_idx", type=int, default=1,
                        help="Start from segment number (1-based)")

    # new
    p_new = sub.add_parser("new", help="Create a new profile")
    p_new.add_argument("profile")
    p_new.add_argument("description", nargs="?", default="")

    # add
    p_add = sub.add_parser("add", help="Add a segment to a profile")
    p_add.add_argument("profile")
    p_add.add_argument("video")
    p_add.add_argument("start", help="e.g. 1:22 or 0:01:22")
    p_add.add_argument("end",   help="e.g. 3:35 or 0:03:35")
    p_add.add_argument("label", nargs="?", default="")

    # show
    p_show = sub.add_parser("show", help="Show profile contents")
    p_show.add_argument("profile")

    # delete
    p_del = sub.add_parser("delete", help="Delete a profile")
    p_del.add_argument("profile")

    # remove segment
    p_rm = sub.add_parser("remove", help="Remove a segment from profile")
    p_rm.add_argument("profile")
    p_rm.add_argument("index", type=int, help="Segment number (1-based)")

    args = parser.parse_args()

    if args.gui or args.cmd is None:
        if HAS_TK:
            gui_main()
        else:
            print("❌  tkinter not available. Use CLI commands instead.")
            parser.print_help()
        return

    if args.cmd == "list":
        profiles = list_profiles()
        if not profiles:
            print("No profiles yet. Create one with:  clip-stacks new <name>")
        else:
            print(f"{'PROFILE':<25}  SEGMENTS")
            print("─" * 40)
            for name in profiles:
                try:
                    p = load_profile(name)
                    n = len(p.get("segments", []))
                    desc = p.get("description", "")
                    print(f"  {name:<23}  {n:>3}  {desc}")
                except Exception:
                    print(f"  {name:<23}  (error reading)")

    elif args.cmd == "play":
        try:
            profile = load_profile(args.profile)
            play_profile(profile, start_index=max(0, args.from_idx - 1))
        except FileNotFoundError as e:
            print(f"❌  {e}")

    elif args.cmd == "new":
        p = new_profile(args.profile)
        p["description"] = args.description
        save_profile(args.profile, p)

    elif args.cmd == "add":
        try:
            try:
                profile = load_profile(args.profile)
            except FileNotFoundError:
                print(f"Profile '{args.profile}' not found, creating it...")
                profile = new_profile(args.profile)
            add_segment(profile, args.video, args.start, args.end, args.label)
            save_profile(args.profile, profile)
            print(f"   Segments now: {len(profile['segments'])}")
        except (ValueError, FileNotFoundError) as e:
            print(f"❌  {e}")

    elif args.cmd == "show":
        try:
            p = load_profile(args.profile)
            print(f"\n📋  Profile: {p['name']}")
            if p.get("description"):
                print(f"    {p['description']}")
            segs = p.get("segments", [])
            if not segs:
                print("    (no segments)")
            else:
                total_dur = sum(s["end"] - s["start"] for s in segs)
                print(f"    {len(segs)} segment(s)  •  total {fmt_time(total_dur)}\n")
                for i, s in enumerate(segs, 1):
                    dur = s["end"] - s["start"]
                    exists = "✅" if os.path.isfile(s["video"]) else "❌"
                    print(f"  {i:>2}.  {exists}  {s.get('label','')}")
                    print(f"       {s['video']}")
                    print(f"       {fmt_time(s['start'])} → {fmt_time(s['end'])}  ({fmt_time(dur)})\n")
        except FileNotFoundError as e:
            print(f"❌  {e}")

    elif args.cmd == "delete":
        p = profile_path(args.profile)
        if p.exists():
            p.unlink()
            print(f"🗑  Profile '{args.profile}' deleted.")
        else:
            print(f"❌  Profile '{args.profile}' not found.")

    elif args.cmd == "remove":
        try:
            profile = load_profile(args.profile)
            idx = args.index - 1
            segs = profile.get("segments", [])
            if 0 <= idx < len(segs):
                removed = segs.pop(idx)
                save_profile(args.profile, profile)
                print(f"🗑  Removed segment #{args.index}: {removed.get('label','')}")
            else:
                print(f"❌  Segment #{args.index} does not exist (profile has {len(segs)}).")
        except FileNotFoundError as e:
            print(f"❌  {e}")


# ─────────────────────────────────────────────────────────────────────────────
# GUI  (tkinter)
# ─────────────────────────────────────────────────────────────────────────────

def gui_main():
    root = tk.Tk()
    app  = ClipStacksApp(root)
    root.mainloop()


class ClipStacksApp:
    BG      = "#0f0f12"
    FG      = "#e8e4d9"
    ACCENT  = "#f5a623"
    DIM     = "#555555"
    GREEN   = "#5dba6e"
    RED     = "#e05252"
    FONT    = ("Courier New", 10)
    BOLD    = ("Courier New", 10, "bold")
    TITLE_F = ("Courier New", 16, "bold")

    def __init__(self, root):
        self.root = root
        self.root.title("Clip Stacks 🎬💪")
        self.root.configure(bg=self.BG)
        self.root.geometry("920x640")
        self.root.resizable(True, True)
        self.current_profile = None
        self._build_ui()
        self._refresh_profiles()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self.root, bg=self.BG)
        hdr.pack(fill="x", padx=20, pady=(18, 0))
        tk.Label(hdr, text="Clip Stacks", font=self.TITLE_F,
                 fg=self.ACCENT, bg=self.BG).pack(side="left")
        tk.Label(hdr, text="  stream your highlights. no fluff.",
                 font=self.FONT, fg=self.DIM, bg=self.BG).pack(side="left", pady=4)

        tk.Frame(self.root, bg=self.ACCENT, height=1).pack(fill="x", padx=20, pady=8)

        pane = tk.PanedWindow(self.root, orient="horizontal",
                              bg=self.BG, sashwidth=4, sashrelief="flat")
        pane.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # ── Left: profile list ──
        left = tk.Frame(pane, bg=self.BG, width=210)
        pane.add(left, minsize=160)

        tk.Label(left, text="PROFILES", font=self.BOLD,
                 fg=self.DIM, bg=self.BG).pack(anchor="w", padx=8, pady=(6,2))

        self.profile_lb = tk.Listbox(left, bg="#1a1a20", fg=self.FG,
                                     selectbackground=self.ACCENT,
                                     selectforeground=self.BG,
                                     font=self.FONT, borderwidth=0,
                                     highlightthickness=0, activestyle="none")
        self.profile_lb.pack(fill="both", expand=True, padx=8)
        self.profile_lb.bind("<<ListboxSelect>>", self._on_profile_select)

        btn_row = tk.Frame(left, bg=self.BG)
        btn_row.pack(fill="x", padx=8, pady=6)
        self._btn(btn_row, "+ New", self._new_profile).pack(side="left")
        self._btn(btn_row, "✕ Del", self._delete_profile, color=self.RED).pack(side="right")

        # ── Right: profile editor ──
        right = tk.Frame(pane, bg=self.BG)
        pane.add(right, minsize=500)

        # Profile name / desc
        info = tk.Frame(right, bg=self.BG)
        info.pack(fill="x", padx=8, pady=4)
        self.name_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        tk.Label(info, text="Name:", font=self.BOLD, fg=self.DIM, bg=self.BG).grid(row=0, column=0, sticky="w")
        tk.Entry(info, textvariable=self.name_var, bg="#1a1a20", fg=self.ACCENT,
                 font=self.BOLD, insertbackground=self.ACCENT, borderwidth=0,
                 highlightthickness=1, highlightcolor=self.ACCENT,
                 highlightbackground="#333").grid(row=0, column=1, sticky="ew", padx=6)
        tk.Label(info, text="Desc:", font=self.FONT, fg=self.DIM, bg=self.BG).grid(row=1, column=0, sticky="w")
        tk.Entry(info, textvariable=self.desc_var, bg="#1a1a20", fg=self.FG,
                 font=self.FONT, insertbackground=self.FG, borderwidth=0,
                 highlightthickness=1, highlightcolor=self.ACCENT,
                 highlightbackground="#333").grid(row=1, column=1, sticky="ew", padx=6)
        info.columnconfigure(1, weight=1)

        tk.Frame(right, bg="#222228", height=1).pack(fill="x", padx=8, pady=4)

        # Segment list
        tk.Label(right, text="SEGMENTS", font=self.BOLD,
                 fg=self.DIM, bg=self.BG).pack(anchor="w", padx=8)

        cols = ("label", "start", "end", "dur", "file")
        self.seg_tree = ttk.Treeview(right, columns=cols, show="headings",
                                     height=10, selectmode="browse")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1a1a20", foreground=self.FG,
                        fieldbackground="#1a1a20", borderwidth=0,
                        rowheight=24, font=self.FONT)
        style.configure("Treeview.Heading",
                        background="#0f0f12", foreground=self.ACCENT,
                        borderwidth=0, font=self.BOLD)
        style.map("Treeview", background=[("selected", "#2a2a35")])

        self.seg_tree.heading("label", text="Label")
        self.seg_tree.heading("start", text="Start")
        self.seg_tree.heading("end",   text="End")
        self.seg_tree.heading("dur",   text="Dur")
        self.seg_tree.heading("file",  text="File")
        self.seg_tree.column("label", width=180)
        self.seg_tree.column("start", width=70, anchor="center")
        self.seg_tree.column("end",   width=70, anchor="center")
        self.seg_tree.column("dur",   width=60, anchor="center")
        self.seg_tree.column("file",  width=220)

        sb = ttk.Scrollbar(right, orient="vertical", command=self.seg_tree.yview)
        self.seg_tree.configure(yscrollcommand=sb.set)
        self.seg_tree.pack(fill="both", expand=True, padx=8)
        sb.pack(side="right", fill="y")

        # Segment add form
        form = tk.LabelFrame(right, text=" Add Segment ",
                             fg=self.ACCENT, bg=self.BG, font=self.FONT,
                             borderwidth=1, relief="solid")
        form.pack(fill="x", padx=8, pady=6)

        self.seg_file  = tk.StringVar()
        self.seg_start = tk.StringVar()
        self.seg_end   = tk.StringVar()
        self.seg_label = tk.StringVar()

        def lbl(t, r, c): tk.Label(form, text=t, font=self.FONT,
                                   fg=self.DIM, bg=self.BG).grid(row=r, column=c, sticky="w", padx=4, pady=2)
        def ent(var, r, c, w=14): tk.Entry(form, textvariable=var, width=w,
                                           bg="#1a1a20", fg=self.FG, insertbackground=self.FG,
                                           font=self.FONT, borderwidth=0,
                                           highlightthickness=1, highlightcolor=self.ACCENT,
                                           highlightbackground="#333").grid(row=r, column=c, padx=4, pady=2, sticky="ew")
        lbl("Video file:", 0, 0)
        fe = tk.Entry(form, textvariable=self.seg_file, bg="#1a1a20", fg=self.FG,
                      font=self.FONT, insertbackground=self.FG, borderwidth=0,
                      highlightthickness=1, highlightcolor=self.ACCENT,
                      highlightbackground="#333")
        fe.grid(row=0, column=1, columnspan=3, sticky="ew", padx=4, pady=2)
        self._btn(form, "Browse", self._browse_video).grid(row=0, column=4, padx=4)

        lbl("Start (M:SS):", 1, 0); ent(self.seg_start, 1, 1, 10)
        lbl("End   (M:SS):", 1, 2); ent(self.seg_end,   1, 3, 10)
        lbl("Label (opt):", 2, 0)
        tk.Entry(form, textvariable=self.seg_label, bg="#1a1a20", fg=self.FG,
                 font=self.FONT, insertbackground=self.FG, borderwidth=0,
                 highlightthickness=1, highlightcolor=self.ACCENT,
                 highlightbackground="#333").grid(row=2, column=1, columnspan=3,
                                                   sticky="ew", padx=4, pady=2)
        form.columnconfigure(1, weight=1)

        add_row = tk.Frame(form, bg=self.BG)
        add_row.grid(row=3, column=0, columnspan=5, pady=4, padx=4, sticky="w")
        self._btn(add_row, "+ Add Segment", self._add_segment, color=self.GREEN).pack(side="left", padx=2)
        self._btn(add_row, "✕ Remove Selected", self._remove_segment, color=self.RED).pack(side="left", padx=2)
        self._btn(add_row, "↑ Move Up", self._move_up).pack(side="left", padx=2)
        self._btn(add_row, "↓ Move Down", self._move_down).pack(side="left", padx=2)

        # Bottom buttons
        tk.Frame(right, bg="#222228", height=1).pack(fill="x", padx=8, pady=4)
        bot = tk.Frame(right, bg=self.BG)
        bot.pack(fill="x", padx=8, pady=(0, 8))
        self._btn(bot, "💾 Save Profile", self._save_profile, color=self.ACCENT).pack(side="left", padx=4)
        self._btn(bot, "▶ Play Profile", self._play_profile, color=self.GREEN, large=True).pack(side="left", padx=4)
        self._btn(bot, "▶ Play from Selected", self._play_from_selected).pack(side="left", padx=4)

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self.root, textvariable=self.status_var,
                 font=self.FONT, fg=self.DIM, bg=self.BG,
                 anchor="w").pack(fill="x", padx=14, pady=(0, 6))

    # ── Widget helper ─────────────────────────────────────────────────────────

    def _btn(self, parent, text, cmd, color=None, large=False):
        c = color or self.FG
        f = ("Courier New", 10, "bold") if large else self.FONT
        return tk.Button(parent, text=text, command=cmd,
                         bg="#1e1e26", fg=c, activebackground="#2a2a38",
                         activeforeground=c, font=f, borderwidth=0,
                         padx=10, pady=4, cursor="hand2",
                         highlightthickness=1, highlightbackground="#333")

    # ── Profile helpers ───────────────────────────────────────────────────────

    def _refresh_profiles(self):
        self.profile_lb.delete(0, "end")
        for name in list_profiles():
            self.profile_lb.insert("end", f"  {name}")

    def _on_profile_select(self, _=None):
        sel = self.profile_lb.curselection()
        if not sel:
            return
        name = self.profile_lb.get(sel[0]).strip()
        try:
            self.current_profile = load_profile(name)
            self.name_var.set(self.current_profile["name"])
            self.desc_var.set(self.current_profile.get("description", ""))
            self._refresh_segments()
            self.status(f"Loaded: {name}")
        except Exception as e:
            self.status(f"❌ {e}")

    def _new_profile(self):
        name = simpledialog.askstring("New Profile", "Profile name:", parent=self.root)
        if not name:
            return
        name = name.strip().replace(" ", "_")
        p = new_profile(name)
        save_profile(name, p)
        self._refresh_profiles()
        self.current_profile = p
        self.name_var.set(name)
        self.desc_var.set("")
        self._refresh_segments()
        self.status(f"Created: {name}")

    def _delete_profile(self):
        if not self.current_profile:
            return
        name = self.current_profile["name"]
        if messagebox.askyesno("Delete", f"Delete profile '{name}'?"):
            profile_path(name).unlink(missing_ok=True)
            self.current_profile = None
            self.name_var.set("")
            self.desc_var.set("")
            self._refresh_segments()
            self._refresh_profiles()
            self.status(f"Deleted: {name}")

    def _save_profile(self):
        if not self.current_profile:
            messagebox.showwarning("No profile", "Select or create a profile first.")
            return
        self.current_profile["name"] = self.name_var.get().strip()
        self.current_profile["description"] = self.desc_var.get().strip()
        save_profile(self.current_profile["name"], self.current_profile)
        self._refresh_profiles()
        self.status(f"Saved: {self.current_profile['name']}")

    # ── Segment helpers ───────────────────────────────────────────────────────

    def _refresh_segments(self):
        self.seg_tree.delete(*self.seg_tree.get_children())
        if not self.current_profile:
            return
        for s in self.current_profile.get("segments", []):
            dur = s["end"] - s["start"]
            fname = Path(s["video"]).name
            exists = "✅" if os.path.isfile(s["video"]) else "❌"
            self.seg_tree.insert("", "end", values=(
                s.get("label", ""),
                fmt_time(s["start"]),
                fmt_time(s["end"]),
                fmt_time(dur),
                f"{exists} {fname}"
            ))

    def _browse_video(self):
        f = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov *.webm *.flv *.m4v"),
                       ("All files", "*.*")]
        )
        if f:
            self.seg_file.set(f)

    def _add_segment(self):
        if not self.current_profile:
            messagebox.showwarning("No profile", "Select or create a profile first.")
            return
        video = self.seg_file.get().strip()
        start = self.seg_start.get().strip()
        end   = self.seg_end.get().strip()
        label = self.seg_label.get().strip()
        if not video or not start or not end:
            messagebox.showerror("Missing fields", "Video file, start, and end are required.")
            return
        try:
            add_segment(self.current_profile, video, start, end, label)
            self._refresh_segments()
            self.seg_file.set("")
            self.seg_start.set("")
            self.seg_end.set("")
            self.seg_label.set("")
            self.status(f"Added segment. Total: {len(self.current_profile['segments'])}")
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror("Error", str(e))

    def _selected_idx(self):
        sel = self.seg_tree.selection()
        if not sel:
            return None
        return self.seg_tree.index(sel[0])

    def _remove_segment(self):
        idx = self._selected_idx()
        if idx is None:
            return
        segs = self.current_profile.get("segments", [])
        if 0 <= idx < len(segs):
            segs.pop(idx)
            self._refresh_segments()
            self.status("Segment removed.")

    def _move_up(self):
        idx = self._selected_idx()
        if idx is None or idx == 0:
            return
        segs = self.current_profile["segments"]
        segs[idx-1], segs[idx] = segs[idx], segs[idx-1]
        self._refresh_segments()
        children = self.seg_tree.get_children()
        if idx-1 < len(children):
            self.seg_tree.selection_set(children[idx-1])

    def _move_down(self):
        idx = self._selected_idx()
        segs = self.current_profile.get("segments", [])
        if idx is None or idx >= len(segs) - 1:
            return
        segs[idx], segs[idx+1] = segs[idx+1], segs[idx]
        self._refresh_segments()
        children = self.seg_tree.get_children()
        if idx+1 < len(children):
            self.seg_tree.selection_set(children[idx+1])

    # ── Playback ──────────────────────────────────────────────────────────────

    def _play_profile(self):
        self._do_play(0)

    def _play_from_selected(self):
        idx = self._selected_idx()
        self._do_play(idx if idx is not None else 0)

    def _do_play(self, start_idx: int):
        if not self.current_profile:
            messagebox.showwarning("No profile", "Select a profile first.")
            return
        try:
            find_mpv()
        except FileNotFoundError as e:
            messagebox.showerror("mpv not found", str(e))
            return
        self._save_profile()
        import threading
        def run():
            play_profile(self.current_profile, start_index=start_idx)
        threading.Thread(target=run, daemon=True).start()
        self.status(f"▶ Playing '{self.current_profile['name']}' from segment #{start_idx+1}…")

    def status(self, msg: str):
        self.status_var.set(msg)
        self.root.update_idletasks()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli_main()
