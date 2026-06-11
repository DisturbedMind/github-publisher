# GitHub Publisher

A beginner-friendly GUI for pushing local project changes to GitHub.

## What You Need First

1. Install Git for Windows: https://git-scm.com/download/win
2. Sign in to GitHub in one of these ways:
   - Install GitHub CLI and run `gh auth login`
   - Or let Git Credential Manager prompt you the first time you push
3. Create an empty repository on GitHub, then copy its HTTPS URL.

## How To Start

Double-click `launch_github_publisher.bat`.

If that does not work, open PowerShell in this folder and run:

```powershell
python .\github_publisher_gui.py
```

## Make A Windows EXE

Double-click `build_exe.bat`.

The first run may download and install PyInstaller. When it finishes, your EXE will be here:

```text
dist\GitHubPublisher.exe
```

You can copy `GitHubPublisher.exe` somewhere convenient, like your Desktop.

Manual PowerShell version:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --noconfirm --name GitHubPublisher --distpath .\dist .\github_publisher_gui.py
```

## Basic Workflow

1. Click **Browse...** and choose your project folder.
2. If it is not a Git repository yet, click **1. Initialize Git**.
3. Paste your GitHub repository URL into **Remote URL**.
4. Click **2. Set Remote**.
5. Click **3. Pull from GitHub** if this GitHub repo already has a README, license, or other files.
6. Write a short commit message, for example `First upload`.
7. Click **Shortcut 4+5. Commit + Push**.

If GitHub rejects the push with `fetch first`, click **3. Pull from GitHub**, then click **5. Push to GitHub** again.

## Notes For Beginners

- A commit is a saved snapshot of your changes.
- Push means upload those saved changes to GitHub.
- Pull means download GitHub's latest commits into your local folder.
- The app stages all changed files with `git add -A`.
- The app does not run destructive Git commands such as reset, clean, or force push.
- If GitHub asks for login, finish the login prompt and then try pushing again.

## Common Errors

`Git was not found`

Install Git for Windows, then close and reopen the app.

`PyInstaller says Access is denied localpycs`

Close VS Code, File Explorer, PowerShell, or antivirus scan windows that may be using the `outputs\build` folder. Run `build_exe.bat` again from a normal non-administrator terminal. The updated builder uses a temporary build folder to avoid the locked `outputs\build\GitHubPublisher\localpycs` path.

If the old build folder is still stuck, restart Windows and delete this folder:

```powershell
Remove-Item -LiteralPath .\build -Recurse -Force
```

`Authentication failed`

Sign in with GitHub CLI using `gh auth login`, or use Git Credential Manager when prompted.

`remote origin already exists`

The app normally handles this by updating the existing `origin` URL when you click **2. Set Remote** or **Shortcut 4+5. Commit + Push**.

`remote: Repository not found`

GitHub cannot find the repository URL currently saved as `origin`, or your GitHub account does not have access to it.

Check the saved URL:

```powershell
git remote -v
```

Create the repository on GitHub first, then copy its HTTPS URL. It should look like this:

```text
https://github.com/DisturbedMind/your-repository-name.git
```

Set the URL:

```powershell
git remote set-url origin https://github.com/DisturbedMind/your-repository-name.git
```

If `origin` does not exist yet, add it instead:

```powershell
git remote add origin https://github.com/DisturbedMind/your-repository-name.git
```

GitHub normally uses `main` as the default branch. If your local branch says `master`, rename it:

```powershell
git branch -M main
git push -u origin main
```

If GitHub still says repository not found, sign in again:

```powershell
gh auth login
```

`nothing to commit`

There are no unsaved local changes. Edit or add a file, click **Refresh**, then try again.

`rejected main -> main (fetch first)`

GitHub already has a commit that your local folder does not have. This often happens when you created the GitHub repository with a README, license, or `.gitignore`.

In the GUI:

1. Click **3. Pull from GitHub**.
2. If Git says `refusing to merge unrelated histories`, click **Fix A. First Upload Pull** once.
3. Click **5. Push to GitHub** again.

In PowerShell:

```powershell
git pull --rebase origin main
git push -u origin main
```

If Git says `refusing to merge unrelated histories`, run this once:

```powershell
git pull --rebase --allow-unrelated-histories origin main
git push -u origin main
```

If Git reports conflicts, open the files it lists, keep the version you want, save them, then run:

```powershell
git add -A
git rebase --continue
git push -u origin main
```

`Pulling is not possible because you have unmerged files`

Git is already paused in the middle of a conflict. Do not pull again yet.

In the GUI:

1. Click **Fix B. Show Conflicts**.
2. Open each listed file.
3. Remove every conflict marker: `<<<<<<<`, `=======`, and `>>>>>>>`.
4. Keep the text you want, then save the file.
5. Click **Fix C. Continue After Fix**.

In PowerShell:

```powershell
git status
```

Open each file listed as `both modified` or `unmerged`, remove the conflict markers, save, then run:

```powershell
git add -A
git rebase --continue
git push -u origin main
```

If you want to cancel the pull/rebase and go back to where you were before resolving conflicts:

```powershell
git rebase --abort
```

`error: could not remove '.git/rebase-merge'`

Windows could not delete Git's temporary rebase folder. This often means an editor, terminal, file explorer window, antivirus scan, or Git process still has something open inside the project.

First close anything opened inside the project folder, then run:

```powershell
git status
```

If Git still says a rebase is in progress and you want to keep going:

```powershell
git add -A
git rebase --continue
```

If Git still says a rebase is in progress and you want to cancel the pull:

```powershell
git rebase --abort
```

If Git says no rebase is in progress but the same cleanup error keeps appearing, restart Windows and try `git status` again. Only after confirming no rebase is in progress, you can remove the stale folder:

```powershell
Remove-Item -LiteralPath .git\rebase-merge -Recurse -Force
git status
```
