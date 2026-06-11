<p align="center">
  <img src="assets/wolf-banner.png" alt="Wolf logo" width="720">
</p>

# GitHub Publisher

GitHub Publisher is a beginner-friendly Windows GUI for publishing local project changes to GitHub without memorizing Git commands.

It is designed for new GitHub users who want a simple workflow:

1. Pick a project folder.
2. Set the GitHub repository URL.
3. Commit changes.
4. Push the project to GitHub.

The app still uses normal Git in the background, but it gives you buttons, status output, and helpful error messages when common Git problems happen.

## Features

- Simple Tkinter desktop GUI
- Numbered workflow buttons for new users
- Shows changed files before committing
- Lets you set or update the `origin` remote URL
- Commits all changed files with `git add -A`
- Pushes to GitHub with upstream tracking
- Pulls remote changes before pushing
- Includes first-upload recovery for repositories created with a README or license
- Helps list and continue after merge conflicts
- Gives beginner-friendly explanations for common Git errors
- Includes a Windows EXE build script using PyInstaller

## Screens And Main Buttons

The normal button sequence is:

1. **Initialize Git**
2. **Set Remote**
3. **Pull from GitHub**
4. **Commit Changes**
5. **Push to GitHub**

There is also a shortcut button:

- **Shortcut 4+5. Commit + Push**

Recovery buttons are marked separately:

- **Fix A. First Upload Pull**
- **Fix B. Show Conflicts**
- **Fix C. Continue After Fix**

## Requirements

- Windows 10 or Windows 11
- Python 3
- Git for Windows
- A GitHub account

Recommended:

- GitHub CLI for easy login

```powershell
gh auth login
```

## Installation

Download or clone this repository.

Install Git for Windows if you do not already have it:

```text
https://git-scm.com/download/win
```

Install Python if you do not already have it:

```text
https://www.python.org/downloads/windows/
```

When installing Python, enable **Add python.exe to PATH**.

## Logo

The wolf logo at the top of this README must exist in the repository at:

```text
assets/wolf-banner.png
```

If the logo is missing on GitHub, copy your wolf image to that exact path, then commit and push it:

```powershell
git add README.md assets/wolf-banner.png
git commit -m "Add wolf logo to README"
git push
```

## Run From Source

From the project folder:

```powershell
python .\github_publisher_gui.py
```

Or double-click:

```text
launch_github_publisher.bat
```

## Build A Windows EXE

Double-click:

```text
build_exe.bat
```

The first build may install PyInstaller.

When the build finishes, the executable will be created here:

```text
dist\GitHubPublisher.exe
```

Manual build command:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --noconfirm --name GitHubPublisher --distpath .\dist .\github_publisher_gui.py
```

## Basic Usage

1. Open GitHub Publisher.
2. Click **Browse...** and choose your project folder.
3. Click **1. Initialize Git** if the folder is not already a Git repository.
4. Paste your GitHub repository HTTPS URL into **Remote URL**.
5. Click **2. Set Remote**.
6. Click **3. Pull from GitHub** if the GitHub repository already contains files.
7. Write a commit message.
8. Click **Shortcut 4+5. Commit + Push**.

## Example GitHub Remote URL

Your remote URL should look like this:

```text
https://github.com/YourUsername/your-repository-name.git
```

If GitHub says `Repository not found`, check that:

- The repository exists on GitHub.
- The spelling and username are correct.
- You are logged into the GitHub account that owns the repository.
- The repository URL ends with `.git`.

## Common Problems

### Git was not found

Install Git for Windows, then close and reopen the app.

### Authentication failed

Sign in to GitHub again:

```powershell
gh auth login
```

You can also use Git Credential Manager when Git prompts for login.

### Repository not found

Check the current remote:

```powershell
git remote -v
```

Set the correct URL:

```powershell
git remote set-url origin https://github.com/YourUsername/your-repository-name.git
```

Then push:

```powershell
git branch -M main
git push -u origin main
```

### Push rejected with fetch first

GitHub has commits that your local folder does not have yet.

In the app:

1. Click **3. Pull from GitHub**.
2. Click **5. Push to GitHub** again.

If the repository was created separately on GitHub with a README or license, click **Fix A. First Upload Pull** once.

### Unmerged files or conflicts

In the app:

1. Click **Fix B. Show Conflicts**.
2. Open each listed file.
3. Remove conflict markers: `<<<<<<<`, `=======`, and `>>>>>>>`.
4. Save the files.
5. Click **Fix C. Continue After Fix**.

### PyInstaller access denied

Run the build from a normal non-administrator terminal. Close editors or File Explorer windows inside the project folder, then run:

```text
build_exe.bat
```

## What This App Does Not Do

This app does not run destructive Git commands such as:

- `git reset --hard`
- `git clean`
- force push

That is intentional. The goal is to keep publishing safer for beginners.

## Project Files

- `github_publisher_gui.py` - main GUI application
- `launch_github_publisher.bat` - simple Windows launcher
- `build_exe.bat` - PyInstaller EXE builder
- `install_wolf_logo.bat` - copies your wolf image to the README logo path
- `assets/wolf-banner.png` - wolf logo shown at the top of this README
- `README.md` - GitHub project README
- `README_GitHub_Publisher.md` - longer local beginner guide

## License

No license has been selected yet. Add a license file before publishing if you want others to reuse or modify this project.
