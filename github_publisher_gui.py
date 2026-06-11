#!/usr/bin/env python3
"""
GitHub Publisher

A beginner-friendly Tkinter GUI for publishing local Git changes.

Requirements:
  - Python 3 with Tkinter
  - Git installed and available on PATH
  - A GitHub account authenticated through Git Credential Manager or GitHub CLI
"""

from __future__ import annotations

import os
import queue
import subprocess
import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_TITLE = "GitHub Publisher"


@dataclass
class GitResult:
    ok: bool
    output: str


class GitHubPublisher(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1120x720")
        self.minsize(980, 620)

        self.repo_path = tk.StringVar()
        self.branch_name = tk.StringVar(value="main")
        self.remote_url = tk.StringVar()
        self.commit_message = tk.StringVar(value="Update project files")
        self.command_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.busy = False

        self._build_ui()
        self._poll_queue()
        self._check_git_available()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        header = ttk.Frame(self, padding=(16, 14, 16, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        title = ttk.Label(header, text=APP_TITLE, font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, sticky="w")

        help_text = (
            "Pick a project folder, review the changed files, write a commit message, "
            "then publish to GitHub."
        )
        help_label = ttk.Label(header, text=help_text, foreground="#444")
        help_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))

        repo_box = ttk.LabelFrame(self, text="Project Folder", padding=12)
        repo_box.grid(row=1, column=0, sticky="ew", padx=16, pady=8)
        repo_box.columnconfigure(1, weight=1)

        ttk.Label(repo_box, text="Folder").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(repo_box, textvariable=self.repo_path).grid(row=0, column=1, sticky="ew")
        ttk.Button(repo_box, text="Browse...", command=self.choose_folder).grid(
            row=0, column=2, padx=(8, 0)
        )
        ttk.Button(repo_box, text="Refresh", command=self.refresh_status).grid(
            row=0, column=3, padx=(8, 0)
        )

        setup_box = ttk.LabelFrame(self, text="Publish Settings", padding=12)
        setup_box.grid(row=2, column=0, sticky="ew", padx=16, pady=8)
        setup_box.columnconfigure(1, weight=1)
        setup_box.columnconfigure(3, weight=1)

        ttk.Label(setup_box, text="Branch").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(setup_box, textvariable=self.branch_name, width=18).grid(
            row=0, column=1, sticky="ew", padx=(0, 12)
        )
        ttk.Label(setup_box, text="Remote URL").grid(row=0, column=2, sticky="w", padx=(0, 8))
        ttk.Entry(setup_box, textvariable=self.remote_url).grid(row=0, column=3, sticky="ew")

        ttk.Label(setup_box, text="Commit Message").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(10, 0)
        )
        ttk.Entry(setup_box, textvariable=self.commit_message).grid(
            row=1, column=1, columnspan=3, sticky="ew", pady=(10, 0)
        )

        main = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main.grid(row=3, column=0, sticky="nsew", padx=16, pady=8)

        changes_box = ttk.LabelFrame(main, text="Changed Files", padding=10)
        changes_box.rowconfigure(0, weight=1)
        changes_box.columnconfigure(0, weight=1)
        self.status_list = tk.Listbox(changes_box, height=12, activestyle="none")
        self.status_list.grid(row=0, column=0, sticky="nsew")
        changes_scroll = ttk.Scrollbar(changes_box, orient=tk.VERTICAL, command=self.status_list.yview)
        changes_scroll.grid(row=0, column=1, sticky="ns")
        self.status_list.configure(yscrollcommand=changes_scroll.set)
        main.add(changes_box, weight=1)

        log_box = ttk.LabelFrame(main, text="Command Log", padding=10)
        log_box.rowconfigure(0, weight=1)
        log_box.columnconfigure(0, weight=1)
        self.log_text = tk.Text(log_box, wrap=tk.WORD, height=12, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll = ttk.Scrollbar(log_box, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=log_scroll.set)
        main.add(log_box, weight=2)

        actions = ttk.Frame(self, padding=(16, 8, 16, 16))
        actions.grid(row=4, column=0, sticky="ew")
        actions.columnconfigure(0, weight=1)

        self.state_label = ttk.Label(actions, text="Ready")
        self.state_label.grid(row=0, column=0, rowspan=2, sticky="w")

        ttk.Button(actions, text="1. Initialize Git", command=self.initialize_repo).grid(
            row=0, column=1, padx=(8, 0)
        )
        ttk.Button(actions, text="2. Set Remote", command=self.set_remote).grid(
            row=0, column=2, padx=(8, 0)
        )
        ttk.Button(actions, text="3. Pull from GitHub", command=self.pull_changes).grid(
            row=0, column=3, padx=(8, 0)
        )
        ttk.Button(
            actions,
            text="Fix A. First Upload Pull",
            command=self.pull_unrelated_changes,
        ).grid(row=0, column=4, padx=(8, 0))
        ttk.Button(actions, text="Fix B. Show Conflicts", command=self.show_conflicts).grid(
            row=0, column=5, padx=(8, 0)
        )
        ttk.Button(actions, text="4. Commit Changes", command=self.commit_changes).grid(
            row=1, column=2, padx=(8, 0), pady=(8, 0)
        )
        ttk.Button(actions, text="5. Push to GitHub", command=self.push_changes).grid(
            row=1, column=3, padx=(8, 0), pady=(8, 0)
        )
        ttk.Button(actions, text="Shortcut 4+5. Commit + Push", command=self.commit_and_push).grid(
            row=1, column=4, padx=(8, 0), pady=(8, 0)
        )
        ttk.Button(
            actions,
            text="Fix C. Continue After Fix",
            command=self.continue_after_conflict_fix,
        ).grid(row=1, column=5, padx=(8, 0), pady=(8, 0))

    def choose_folder(self) -> None:
        folder = filedialog.askdirectory(title="Choose your project folder")
        if folder:
            self.repo_path.set(folder)
            self.refresh_status()

    def _check_git_available(self) -> None:
        result = self.run_git(["--version"], cwd=None)
        if result.ok:
            self.append_log(result.output.strip())
        else:
            messagebox.showerror(
                APP_TITLE,
                "Git was not found. Install Git for Windows first, then reopen this app.",
            )

    def validate_folder(self) -> Path | None:
        folder = self.repo_path.get().strip()
        if not folder:
            messagebox.showwarning(APP_TITLE, "Choose a project folder first.")
            return None
        path = Path(folder)
        if not path.exists() or not path.is_dir():
            messagebox.showwarning(APP_TITLE, "The selected project folder does not exist.")
            return None
        return path

    def run_git(self, args: list[str], cwd: Path | None) -> GitResult:
        try:
            env = os.environ.copy()
            env.setdefault("GIT_EDITOR", "true")
            completed = subprocess.run(
                ["git", *args],
                cwd=str(cwd) if cwd else None,
                env=env,
                text=True,
                capture_output=True,
                check=False,
                shell=False,
            )
        except FileNotFoundError:
            return GitResult(False, "Git was not found on PATH.")
        output = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
        return GitResult(completed.returncode == 0, output)

    def run_git_logged(self, args: list[str], cwd: Path) -> GitResult:
        self.append_log(f"\n$ git {' '.join(args)}")
        result = self.run_git(args, cwd)
        if result.output:
            self.append_log(result.output)
        return result

    def enqueue_git(self, title: str, steps: list[list[str]], refresh_after: bool = True) -> None:
        path = self.validate_folder()
        if not path or self.busy:
            return

        def worker() -> None:
            self.command_queue.put(("state", title))
            ok = True
            for step in steps:
                self.command_queue.put(("log", f"\n$ git {' '.join(step)}"))
                result = self.run_git(step, path)
                if result.output:
                    self.command_queue.put(("log", result.output))
                if not result.ok:
                    guidance = self.guidance_for_error(result.output)
                    if guidance:
                        self.command_queue.put(("log", guidance))
                    ok = False
                    break
            self.command_queue.put(("state", "Ready" if ok else "Stopped after an error"))
            if refresh_after:
                self.command_queue.put(("refresh", ""))

        self.busy = True
        threading.Thread(target=worker, daemon=True).start()

    def guidance_for_error(self, output: str) -> str:
        lowered = output.lower()
        if "repository not found" in lowered:
            return (
                "\nHelp: GitHub cannot find that repository URL, or your account does not "
                "have access. Create the repository on GitHub first, copy its HTTPS URL, "
                "paste it into 'Remote URL', click '2. Set Remote', then push again. Also "
                "check that you are signed in to the right GitHub account."
            )
        if "could not remove" in lowered and ".git/rebase-merge" in lowered:
            return (
                "\nHelp: Windows could not remove Git's temporary rebase folder. "
                "Close editors, terminals, and file explorer windows opened inside this "
                "project, then run 'git status'. If Git says no rebase is in progress but "
                "the folder is still stuck, restart Windows and try again."
            )
        if "fetch first" in lowered or "updates were rejected" in lowered:
            return (
                "\nHelp: GitHub already has commits that are not in this folder. "
                "Click '3. Pull from GitHub', fix any conflicts if Git asks, then push again. "
                "If this is your first upload and the GitHub repo was created with a README "
                "or license, use 'Fix A. First Upload Pull' once."
            )
        if "refusing to merge unrelated histories" in lowered:
            return (
                "\nHelp: Your local folder and the GitHub repo were started separately. "
                "Use 'Fix A. First Upload Pull' once, then push again."
            )
        if "merge conflict" in lowered or "conflict" in lowered:
            return (
                "\nHelp: Git found conflicting edits. Click 'Fix B. Show Conflicts' to list the "
                "files. Open those files, remove the <<<<<<<, =======, and >>>>>>> markers, "
                "save them, then click 'Fix C. Continue After Fix'."
            )
        if "no rebase in progress" in lowered:
            return (
                "\nHelp: Git is not in a rebase. If you fixed merge conflicts, click "
                "'4. Commit Changes', then '5. Push to GitHub'."
            )
        return ""

    def refresh_status(self) -> None:
        path = self.validate_folder()
        if not path:
            return

        self.status_list.delete(0, tk.END)

        inside = self.run_git(["rev-parse", "--is-inside-work-tree"], path)
        if not inside.ok:
            self.status_list.insert(tk.END, "This folder is not a Git repository yet.")
            self.append_log("This folder is not a Git repository yet. Use 1. Initialize Git.")
            self.state_label.configure(text="Not a Git repository")
            return

        branch = self.run_git(["branch", "--show-current"], path)
        if branch.ok and branch.output.strip():
            self.branch_name.set(branch.output.strip())

        remote = self.run_git(["remote", "get-url", "origin"], path)
        if remote.ok and remote.output.strip():
            self.remote_url.set(remote.output.strip())

        status = self.run_git(["status", "--short"], path)
        self.status_list.delete(0, tk.END)
        if status.ok and status.output.strip():
            for line in status.output.splitlines():
                self.status_list.insert(tk.END, line)
            if self.has_unmerged_files(status.output):
                self.state_label.configure(text="Conflicts need fixing")
                self.append_log(
                    "Conflicts detected. Click 'Fix B. Show Conflicts', fix the files, then "
                    "click 'Fix C. Continue After Fix'."
                )
            else:
                self.state_label.configure(text="Changes found")
        elif status.ok:
            self.status_list.insert(tk.END, "No local changes.")
            self.state_label.configure(text="Clean working tree")
        else:
            self.status_list.insert(tk.END, status.output or "Unable to read Git status.")
            self.state_label.configure(text="Status failed")

    def initialize_repo(self) -> None:
        branch = self.branch_name.get().strip() or "main"
        self.enqueue_git("Initializing Git...", [["init"], ["branch", "-M", branch]])

    def set_remote(self) -> None:
        path = self.validate_folder()
        if not path:
            return
        remote = self.remote_url.get().strip()
        if not remote:
            messagebox.showwarning(APP_TITLE, "Paste your GitHub repository URL first.")
            return
        inside = self.run_git(["rev-parse", "--is-inside-work-tree"], path)
        if not inside.ok:
            messagebox.showwarning(APP_TITLE, "Use 1. Initialize Git before setting a remote URL.")
            return

        exists = self.run_git(["remote", "get-url", "origin"], path)
        if exists.ok:
            steps = [["remote", "set-url", "origin", remote]]
        else:
            steps = [["remote", "add", "origin", remote]]
        self.enqueue_git("Saving remote URL...", steps)

    def commit_changes(self) -> None:
        message = self.commit_message.get().strip()
        if not message:
            messagebox.showwarning(APP_TITLE, "Write a commit message first.")
            return
        self.enqueue_git("Committing changes...", [["add", "-A"], ["commit", "-m", message]])

    def has_unmerged_files(self, status_output: str) -> bool:
        conflict_codes = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
        for line in status_output.splitlines():
            if len(line) >= 2 and line[:2] in conflict_codes:
                return True
        return False

    def show_conflicts(self) -> None:
        path = self.validate_folder()
        if not path:
            return
        result = self.run_git(["diff", "--name-only", "--diff-filter=U"], path)
        self.append_log("\n$ git diff --name-only --diff-filter=U")
        if result.output:
            self.append_log(result.output)
        if result.ok and result.output.strip():
            self.status_list.delete(0, tk.END)
            for filename in result.output.splitlines():
                self.status_list.insert(tk.END, f"CONFLICT  {filename}")
            self.state_label.configure(text="Conflicts need fixing")
            self.append_log(
                "\nOpen each listed file and remove conflict markers: <<<<<<<, =======, >>>>>>>. "
                "Keep the version you want, save the file, then click 'Fix C. Continue After Fix'."
            )
        elif result.ok:
            self.append_log("No conflicted files found.")
        else:
            self.append_log(result.output or "Unable to list conflicted files.")

    def continue_after_conflict_fix(self) -> None:
        path = self.validate_folder()
        if not path:
            return
        markers_left = self.files_with_conflict_markers(path)
        if markers_left:
            messagebox.showwarning(
                APP_TITLE,
                "These files still contain conflict markers:\n\n"
                + "\n".join(markers_left[:10])
                + "\n\nRemove every <<<<<<<, =======, and >>>>>>> marker, save, then try again.",
            )
            return
        branch = self.branch_name.get().strip() or "main"
        self.enqueue_git(
            "Continuing after conflict fix...",
            [["add", "-A"], ["rebase", "--continue"], ["push", "-u", "origin", branch]],
        )

    def files_with_conflict_markers(self, path: Path) -> list[str]:
        conflicted = self.run_git(["diff", "--name-only", "--diff-filter=U"], path)
        if not conflicted.ok or not conflicted.output.strip():
            return []
        files: list[str] = []
        marker_text = ("<<<<<<<", "=======", ">>>>>>>")
        for relative_name in conflicted.output.splitlines():
            file_path = path / relative_name
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if any(marker in text for marker in marker_text):
                files.append(relative_name)
        return files

    def pull_changes(self) -> None:
        branch = self.branch_name.get().strip() or "main"
        self.enqueue_git("Pulling from GitHub...", [["pull", "--rebase", "origin", branch]])

    def pull_unrelated_changes(self) -> None:
        branch = self.branch_name.get().strip() or "main"
        confirmed = messagebox.askyesno(
            APP_TITLE,
            "Use this only when your local folder and GitHub repo were started separately, "
            "for example when GitHub already has a README or license. Continue?",
        )
        if not confirmed:
            return
        self.enqueue_git(
            "Pulling first-upload GitHub files...",
            [["pull", "--rebase", "--allow-unrelated-histories", "origin", branch]],
        )

    def push_changes(self) -> None:
        branch = self.branch_name.get().strip() or "main"
        self.enqueue_git("Pushing to GitHub...", [["push", "-u", "origin", branch]])

    def commit_and_push(self) -> None:
        path = self.validate_folder()
        if not path:
            return

        remote = self.remote_url.get().strip()
        message = self.commit_message.get().strip()
        branch = self.branch_name.get().strip() or "main"
        if not message:
            messagebox.showwarning(APP_TITLE, "Write a commit message first.")
            return
        if not remote:
            messagebox.showwarning(APP_TITLE, "Paste your GitHub repository URL first.")
            return

        steps: list[list[str]] = []
        inside = self.run_git(["rev-parse", "--is-inside-work-tree"], path)
        if not inside.ok:
            steps.append(["init"])

        remote_exists = self.run_git(["remote", "get-url", "origin"], path)
        remote_step = (
            ["remote", "set-url", "origin", remote]
            if remote_exists.ok
            else ["remote", "add", "origin", remote]
        )
        steps.extend(
            [
                ["branch", "-M", branch],
                remote_step,
                ["add", "-A"],
                ["commit", "-m", message],
                ["push", "-u", "origin", branch],
            ]
        )
        self.enqueue_git(
            "Committing and pushing...",
            steps,
        )

    def append_log(self, text: str) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + os.linesep)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _poll_queue(self) -> None:
        try:
            while True:
                kind, payload = self.command_queue.get_nowait()
                if kind == "log":
                    self.append_log(payload)
                elif kind == "state":
                    self.state_label.configure(text=payload)
                    if payload in {"Ready", "Stopped after an error"}:
                        self.busy = False
                elif kind == "refresh":
                    self.refresh_status()
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)


def main() -> None:
    app = GitHubPublisher()
    app.mainloop()


if __name__ == "__main__":
    main()
