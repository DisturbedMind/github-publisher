<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="GUI" src="https://img.shields.io/badge/GUI-local%20web-0f766e">
  <img alt="Git" src="https://img.shields.io/badge/Git-supported-F05032?logo=git&logoColor=white">
  <img alt="GitHub CLI" src="https://img.shields.io/badge/GitHub%20CLI-gh-181717?logo=github&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white">
</p>

<p align="center">
  <img src="assets/wolf-banner.png" alt="Wolf logo" width="720">
</p>

# GitHub Publisher GUI

A local, dependency-light GUI for publishing existing project folders to GitHub.

It runs as a small Python web app on your machine and calls the installed `git`
and GitHub CLI (`gh`) tools only when you click an action.

## Features

- Browse for a local project folder or paste a path manually
- Inspect branch, remote, and changed files
- Stage or unstage individual files
- Initialize Git in a selected folder
- Set or update the `origin` remote URL
- Pull from GitHub with rebase
- Run the first-upload pull for unrelated histories
- Show conflicted files
- Continue after conflict markers are removed
- Commit all changes and push in one shortcut
- Create a GitHub repository with `gh repo create`
- Commit staged changes
- Push to the selected remote and branch
- Open the published repository in your browser
- Keep an on-screen action log of every command result

## Requirements

- Python 3.10+
- Git installed and available on `PATH`
- GitHub CLI installed and authenticated:

```powershell
gh auth login
```

## Run

```powershell
cd C:\Codex\Projects\github-publisher-gui
python .\app.py
```

Then open:

```text
http://127.0.0.1:8765
```

## Notes

- The app never stores GitHub tokens.
- Commands run only inside the project path you enter.
- If the repository does not exist yet, use **Create repository** first.
- If the project is not a Git repo yet, choose the folder and click **1. Initialize Git**.
- If GitHub rejects your push because the remote has a README, license, or `.gitignore`,
  click **3. Pull from GitHub**. If Git says the histories are unrelated, click
  **Fix A. First Upload Pull** once.
- If Git reports conflicts, click **Fix B. Show Conflicts**, edit the listed files,
  remove every `<<<<<<<`, `=======`, and `>>>>>>>` marker, save, then click
  **Fix C. Continue After Fix**.

