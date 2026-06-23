<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="GUI" src="https://img.shields.io/badge/GUI-Tkinter%20desktop-0f766e">
  <img alt="Git" src="https://img.shields.io/badge/Git-supported-F05032?logo=git&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white">
</p>

<p align="center">
  <img src="assets/wolf-banner.png" alt="Wolf logo" width="720">
</p>

# GitHub Publisher GUI

A small Windows desktop app for publishing existing project folders to GitHub.

It uses a local Tkinter interface with the same wolf-branded look as **YouTube Music Playlist Downloader**. Commands run only when you click an action, and every Git result is shown in the command log.

## What You Need

- Windows
- Git installed and available on `PATH`
- GitHub CLI (`gh`) installed and available on `PATH` if you want to use the in-app **GitHub Login** button
- Python 3.10+ only if you want to run from source instead of the bundled EXE

## Quick Start

Download or clone this repository, then run:

```text
dist\GitHubPublisher.exe
```

If Windows SmartScreen warns about an unknown publisher, choose **More info** and **Run anyway** only if you downloaded it from the repository you trust.

## Run From Source

Clone the repo into any folder you like:

```powershell
git clone https://github.com/DisturbedMind/GitHub-Publisher.git
cd GitHub-Publisher
python .\github_publisher_gui.py
```

Or, from inside the cloned folder:

```powershell
.\run.ps1
```

## Build The EXE

```powershell
.\build_exe.bat
```

The rebuilt app is written to:

```text
dist\GitHubPublisher.exe
```

## Features

- Sign in with GitHub from the app through GitHub CLI
- Check the current GitHub login status
- Browse for a local project folder or paste a path manually
- Inspect branch, remote, and changed files
- Initialize Git in a selected folder
- Set or update the `origin` remote URL
- Pull from GitHub with rebase
- Run the first-upload pull for unrelated histories
- Show conflicted files
- Continue after conflict markers are removed
- Commit all changes and push in one shortcut
- Push to the selected remote and branch
- Keep an on-screen action log of every command result

## Notes

- The app never stores GitHub tokens; GitHub CLI handles authentication.
- Commands run only inside the project path you enter.
- If the project is not a Git repo yet, choose the folder and click **1. Initialize Git**.
- If GitHub rejects your push because the remote already has a README, license, or `.gitignore`, click **3. Pull from GitHub**. If Git says the histories are unrelated, click **Fix A. First Upload Pull** once.
- If Git reports conflicts, click **Fix B. Show Conflicts**, edit the listed files, remove every `<<<<<<<`, `=======`, and `>>>>>>>` marker, save, then click **Fix C. Continue After Fix**.
