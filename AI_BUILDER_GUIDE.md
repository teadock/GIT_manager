# AI Builder Guide: GitHub Repository Manager

## Overview

This guide is for AI assistants recreating the GitHub Repository Manager on different platforms (Windows, Linux). It contains all critical implementation details, gotchas, and platform-specific requirements.

---

## 1. CRITICAL REQUIREMENTS

### Assets Needed

1. **GitHub Logo**
   - Source: https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png
   - Original format: PNG, transparent background
   - Required conversions:
     - **Windows**: Convert to .ico (256x256, 128x128, 64x64, 32x32, 16x16 sizes)
     - **macOS**: Convert to .icns (all standard sizes: 16, 32, 64, 128, 256, 512, 1024 with @2x retina)
     - **Linux**: Keep as .png (256x256 or 128x128)

   **Conversion Tools:**
   - Online: https://convertio.co/png-ico/ or https://anyconv.com/png-to-icns-converter/
   - Command line (macOS): `sips -s format icns input.png --out output.icns`
   - Command line (Linux): ImageMagick: `convert -resize 256x256 input.png output.ico`

2. **Python Script**
   - Single file: `github_manager.py`
   - Pure Python 3.8+ with Tkinter (standard library)
   - No external dependencies except GitHub CLI

---

## 2. SSH SETUP (CRITICAL FOR ALL PLATFORMS)

### Why SSH is Required

- GitHub CLI can use HTTPS or SSH
- HTTPS requires password/token on every operation
- SSH uses key-based authentication (no prompts)
- This app assumes SSH protocol for all repo operations

### Complete SSH Configuration

#### Step 1: Generate SSH Key

```bash
# Use Ed25519 (modern, secure)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Or RSA if Ed25519 not supported
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**Prompts:**
- File location: Press Enter (default: `~/.ssh/id_ed25519`)
- Passphrase: Optional (can leave empty for convenience)

**Files created:**
- `~/.ssh/id_ed25519` (private key - NEVER share)
- `~/.ssh/id_ed25519.pub` (public key - add to GitHub)

#### Step 2: Start SSH Agent

**macOS/Linux:**
```bash
eval "$(ssh-agent -s)"
```

**Windows (Git Bash):**
```bash
eval $(ssh-agent -s)
```

**Windows (PowerShell):**
```powershell
# Add to PowerShell profile for auto-start
Start-Service ssh-agent
```

#### Step 3: Add Key to Agent

**macOS:**
```bash
# Stores passphrase in macOS Keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

**Windows/Linux:**
```bash
ssh-add ~/.ssh/id_ed25519
```

#### Step 4: Copy Public Key

**macOS:**
```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

**Windows (PowerShell):**
```powershell
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
```

**Windows (Git Bash):**
```bash
cat ~/.ssh/id_ed25519.pub | clip
```

**Linux:**
```bash
# With xclip
sudo apt install xclip
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard

# Or manually
cat ~/.ssh/id_ed25519.pub
# Then Ctrl+Shift+C to copy
```

#### Step 5: Add to GitHub

1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Title: e.g., "MacBook Pro" or "Windows Desktop"
4. Key type: Authentication Key
5. Paste public key content
6. Click "Add SSH key"
7. Confirm with password if prompted

#### Step 6: Test SSH Connection

```bash
ssh -T git@github.com
```

**Expected output:**
```
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

**If you see "Permission denied":**
- Check key was added to GitHub
- Check key is in ssh-agent: `ssh-add -l`
- Check SSH config: `cat ~/.ssh/config`

#### Step 7: Configure Git to Use SSH

```bash
# Set SSH as default protocol
gh config set git_protocol ssh

# Or globally for git
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

---

## 3. GITHUB CLI AUTHENTICATION

### Installation

**macOS:**
```bash
brew install gh
```

**Windows:**
```powershell
# Using winget
winget install --id GitHub.cli

# Or download from: https://cli.github.com/
```

**Linux (Debian/Ubuntu):**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install gh
```

### Initial Authentication

```bash
gh auth login
```

**Interactive prompts:**
1. **What account do you want to log into?**
   → GitHub.com

2. **What is your preferred protocol for Git operations?**
   → SSH ⚠️ CRITICAL: Must choose SSH

3. **Upload your SSH public key to your GitHub account?**
   → Yes (select your ~/.ssh/id_ed25519.pub)
   → Or skip if already added manually

4. **How would you like to authenticate?**
   → Login with a web browser

5. **One-time code:**
   → Copy the code shown (e.g., A1B2-C3D4)
   → Press Enter to open browser
   → Paste code in browser
   → Authorize GitHub CLI

### Grant Delete Permission

**CRITICAL:** Default scopes don't include repository deletion.

```bash
gh auth refresh -h github.com -s delete_repo
```

**This command:**
- Opens browser for authentication
- Shows one-time code
- Grants `delete_repo` scope to your token

**Verification:**
```bash
gh auth status
```

**Expected output:**
```
github.com
  ✓ Logged in to github.com account USERNAME (keyring)
  - Active account: true
  - Git operations protocol: ssh
  - Token: gho_************************************
  - Token scopes: 'admin:public_key', 'delete_repo', 'gist', 'read:org', 'repo'
```

**Must see:**
- ✓ Logged in (checkmark)
- `delete_repo` in Token scopes
- Git operations protocol: ssh

---

## 4. CODE MODIFICATIONS (PLATFORM-SPECIFIC)

### Finding GitHub CLI Path

**macOS:**
```bash
which gh
# Common paths:
# /opt/homebrew/bin/gh (Apple Silicon)
# /usr/local/bin/gh (Intel Mac)
```

**Windows:**
```powershell
where gh
# Common paths:
# C:\Program Files\GitHub CLI\gh.exe
# C:\Users\USERNAME\AppData\Local\Programs\GitHub CLI\gh.exe
```

**Linux:**
```bash
which gh
# Common paths:
# /usr/bin/gh
# /usr/local/bin/gh
```

### Update GH_PATH Constant

**Line 14 in `github_manager.py`:**

```python
# macOS (Homebrew on Apple Silicon)
GH_PATH = '/opt/homebrew/bin/gh'

# macOS (Homebrew on Intel)
GH_PATH = '/usr/local/bin/gh'

# Windows
GH_PATH = r'C:\Program Files\GitHub CLI\gh.exe'

# Linux
GH_PATH = '/usr/bin/gh'
```

**⚠️ CRITICAL:** Use raw string `r'...'` on Windows to handle backslashes.

### Update Username for Delete

**Line 229 in `delete_repository` method:**

```python
# Original (hardcoded for user 'teadock')
subprocess.run(
    [GH_PATH, 'repo', 'delete', f'teadock/{name}', '--yes'],
    ...
)

# Change 'teadock' to actual username
subprocess.run(
    [GH_PATH, 'repo', 'delete', f'YOUR_GITHUB_USERNAME/{name}', '--yes'],
    ...
)
```

**How to get username:**
```bash
gh api user --jq .login
```

**Or make it dynamic:**
```python
# At top of file, after imports
import subprocess
result = subprocess.run([GH_PATH, 'api', 'user', '--jq', '.login'], 
                       capture_output=True, text=True)
GITHUB_USERNAME = result.stdout.strip()

# Then in delete_repository:
subprocess.run(
    [GH_PATH, 'repo', 'delete', f'{GITHUB_USERNAME}/{name}', '--yes'],
    ...
)
```

---

## 5. PLATFORM-SPECIFIC PACKAGING

### macOS (.app Bundle)

#### Structure
```
GitHubManager.app/
├── Contents/
│   ├── Info.plist          (metadata)
│   ├── MacOS/
│   │   └── GitHubManager   (executable Python script)
│   └── Resources/
│       └── AppIcon.icns    (icon file)
```

#### Creation Script

```bash
#!/bin/bash

APP_NAME="GitHubManager"
APP_DIR="$HOME/Desktop/${APP_NAME}.app"

# Create structure
mkdir -p "${APP_DIR}/Contents/MacOS"
mkdir -p "${APP_DIR}/Contents/Resources"

# Copy Python script
cp github_manager.py "${APP_DIR}/Contents/MacOS/${APP_NAME}"
chmod +x "${APP_DIR}/Contents/MacOS/${APP_NAME}"

# Create Info.plist
cat > "${APP_DIR}/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>GitHubManager</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.github.manager</string>
    <key>CFBundleName</key>
    <string>GitHub Manager</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
</dict>
</plist>
EOF

# Copy icon (if available)
if [ -f github_logo.icns ]; then
    cp github_logo.icns "${APP_DIR}/Contents/Resources/AppIcon.icns"
fi

echo "✅ App bundle created at: ${APP_DIR}"
```

#### Info.plist Keys Explained

- `CFBundleExecutable`: Name of executable file in MacOS folder
- `CFBundleIconFile`: Icon filename (without .icns extension)
- `CFBundleIdentifier`: Reverse DNS (com.yourname.appname)
- `CFBundleName`: Display name in Finder
- `CFBundlePackageType`: Always "APPL" for applications
- `CFBundleShortVersionString`: User-facing version
- `CFBundleVersion`: Build number

### Windows (.exe with PyInstaller)

#### Prerequisites

```powershell
pip install pyinstaller
```

#### Build Command

```powershell
pyinstaller `
  --onefile `
  --windowed `
  --icon=github_logo.ico `
  --name="GitHub Manager" `
  github_manager.py
```

**Flags explained:**
- `--onefile`: Single .exe (no dependencies folder)
- `--windowed`: No console window (GUI only)
- `--icon=github_logo.ico`: Application icon
- `--name`: Output filename

**Output:**
- `dist/GitHub Manager.exe` (distributable executable)

#### Advanced: Spec File Customization

```python
# github_manager.spec (auto-generated, can edit)

a = Analysis(
    ['github_manager.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GitHub Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='github_logo.ico',  # Icon path
)
```

**Rebuild with spec:**
```powershell
pyinstaller github_manager.spec
```

#### Creating Installer (Optional)

Use **Inno Setup** for professional installer:

1. Download: https://jrsoftware.org/isinfo.php
2. Create script: `installer.iss`

```ini
[Setup]
AppName=GitHub Manager
AppVersion=1.0
DefaultDirName={pf}\GitHub Manager
DefaultGroupName=GitHub Manager
OutputDir=installer_output
OutputBaseFilename=GitHubManager_Setup

[Files]
Source: "dist\GitHub Manager.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\GitHub Manager"; Filename: "{app}\GitHub Manager.exe"
Name: "{commondesktop}\GitHub Manager"; Filename: "{app}\GitHub Manager.exe"
```

3. Compile with Inno Setup Compiler
4. Output: `installer_output/GitHubManager_Setup.exe`

### Linux (.desktop Entry)

#### System-wide Installation

```bash
#!/bin/bash

# Copy script to system bin
sudo cp github_manager.py /usr/local/bin/github-manager
sudo chmod +x /usr/local/bin/github-manager

# Copy icon (optional)
sudo mkdir -p /usr/share/pixmaps
sudo cp github_logo.png /usr/share/pixmaps/github-manager.png

# Create desktop entry
cat > ~/.local/share/applications/github-manager.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=GitHub Manager
Comment=Manage GitHub repositories
Exec=/usr/local/bin/github-manager
Icon=github-manager
Terminal=false
Categories=Development;Utility;
StartupNotify=true
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/

echo "✅ Desktop entry created"
```

#### Desktop Entry Keys Explained

- `Version`: Desktop Entry Specification version (not app version)
- `Type`: Always "Application"
- `Name`: Display name in app menus
- `Comment`: Tooltip description
- `Exec`: Command to run (absolute path)
- `Icon`: Icon name or path (no extension)
- `Terminal`: false = GUI, true = run in terminal
- `Categories`: Menu categorization (semicolon-separated)
- `StartupNotify`: Show "launching" feedback

#### Categories Reference

Common categories:
- `Development` - Programming tools
- `Utility` - System utilities
- `Network` - Network applications
- `Office` - Productivity apps

---

## 6. TESTING CHECKLIST

### Pre-Launch Tests

- [ ] `gh --version` shows installed version
- [ ] `gh auth status` shows authenticated with SSH
- [ ] `gh auth status` includes `delete_repo` scope
- [ ] `ssh -T git@github.com` authenticates successfully
- [ ] `which gh` (or `where gh`) shows correct path
- [ ] `GH_PATH` in code matches actual path
- [ ] Username in delete function is correct

### Functional Tests

- [ ] App launches without errors
- [ ] Window appears with correct size (700x600)
- [ ] Repository list loads automatically
- [ ] Repos shown sorted by push date (newest first)
- [ ] Each card shows: name, size, date, privacy
- [ ] Typing in text field works
- [ ] Pressing Enter creates repository
- [ ] Clicking "Create New" creates repository
- [ ] New repo appears in list immediately
- [ ] Repo name copied to clipboard after creation
- [ ] Delete button shows confirmation dialog
- [ ] Confirming delete removes repo from GitHub
- [ ] List refreshes after deletion
- [ ] Canceling delete keeps repository
- [ ] Invalid names show error message
- [ ] Empty name shows warning

### SSH Protocol Verification

```bash
# Create test repo via app
# Then check its remote URL:

gh repo view YOUR_USERNAME/test-repo --json url --jq .url

# Should show SSH URL:
# ✅ git@github.com:YOUR_USERNAME/test-repo.git
# ❌ https://github.com/YOUR_USERNAME/test-repo.git

# If HTTPS shown, fix with:
gh config set git_protocol ssh
```

### Error Handling Tests

- [ ] Network error shows clear message
- [ ] `gh` not found shows helpful error
- [ ] Authentication failure shows login instructions
- [ ] Missing `delete_repo` scope shows auth refresh command
- [ ] Invalid repo name shows format requirements
- [ ] Duplicate repo name shows GitHub error

---

## 7. COMMON PITFALLS & SOLUTIONS

### Problem: "gh: command not found"

**Cause:** GitHub CLI not installed or not in PATH

**Solution:**
1. Install GitHub CLI for your platform
2. Verify: `gh --version`
3. If still not found, use absolute path in code

### Problem: "Permission Required - delete_repo scope"

**Cause:** GitHub CLI token missing deletion permission

**Solution:**
```bash
gh auth refresh -h github.com -s delete_repo
```

This is **required** - deletion won't work without it.

### Problem: Repos created with HTTPS instead of SSH

**Cause:** GitHub CLI configured for HTTPS protocol

**Solution:**
```bash
gh config set git_protocol ssh
```

**Verification:**
```bash
gh config get git_protocol
# Should output: ssh
```

### Problem: App won't start on macOS

**Cause:** Script not executable

**Solution:**
```bash
chmod +x ~/Desktop/GitHubManager.app/Contents/MacOS/GitHubManager
```

### Problem: "tkinter.TclError: no display name and no $DISPLAY environment variable"

**Cause:** Running on headless system or over SSH without X11

**Solution:**
- Use system with GUI
- Or enable X11 forwarding: `ssh -X user@host`

### Problem: ModuleNotFoundError: No module named 'tkinter'

**Cause:** Python built without Tkinter support

**Solution:**

**macOS:**
```bash
# Reinstall Python with Tkinter
brew reinstall python-tk
```

**Windows:**
- Tkinter included by default
- Reinstall Python and check "tcl/tk" option

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

### Problem: Icon doesn't show on macOS

**Cause:** Wrong icon format or filename

**Solution:**
1. Icon must be .icns format
2. Must be named `AppIcon.icns` (matches Info.plist)
3. Must be in `Contents/Resources/` folder

**Convert PNG to ICNS:**
```bash
mkdir AppIcon.iconset
sips -z 16 16 github_logo.png --out AppIcon.iconset/icon_16x16.png
sips -z 32 32 github_logo.png --out AppIcon.iconset/icon_16x16@2x.png
sips -z 32 32 github_logo.png --out AppIcon.iconset/icon_32x32.png
sips -z 64 64 github_logo.png --out AppIcon.iconset/icon_32x32@2x.png
sips -z 128 128 github_logo.png --out AppIcon.iconset/icon_128x128.png
sips -z 256 256 github_logo.png --out AppIcon.iconset/icon_128x128@2x.png
sips -z 256 256 github_logo.png --out AppIcon.iconset/icon_256x256.png
sips -z 512 512 github_logo.png --out AppIcon.iconset/icon_256x256@2x.png
sips -z 512 512 github_logo.png --out AppIcon.iconset/icon_512x512.png
cp github_logo.png AppIcon.iconset/icon_512x512@2x.png
iconutil -c icns AppIcon.iconset
```

### Problem: Icon doesn't show on Windows

**Cause:** Wrong icon format

**Solution:**
1. Icon must be .ico format (not .png)
2. Should contain multiple sizes (256, 128, 64, 32, 16)
3. Use proper icon editor or converter

**Convert with ImageMagick:**
```bash
convert github_logo.png -define icon:auto-resize=256,128,64,32,16 github_logo.ico
```

### Problem: Delete fails - "Resource not accessible by integration"

**Cause:** Token doesn't have admin rights to repository

**Solution:**
1. Verify you own the repository
2. Check `delete_repo` scope: `gh auth status`
3. Re-authenticate if needed: `gh auth refresh -h github.com -s delete_repo`

### Problem: Username hardcoded causes delete to fail

**Cause:** Line 229 uses wrong username

**Solution:**
```python
# Get username dynamically
result = subprocess.run(
    [GH_PATH, 'api', 'user', '--jq', '.login'],
    capture_output=True, text=True, check=True
)
username = result.stdout.strip()

# Use in delete
subprocess.run(
    [GH_PATH, 'repo', 'delete', f'{username}/{name}', '--yes'],
    ...
)
```

---

## 8. DISTRIBUTION CHECKLIST

### For End Users

**What to provide:**
- [ ] Executable file (.app, .exe, or .desktop)
- [ ] README with prerequisites
- [ ] Setup instructions for GitHub CLI
- [ ] SSH setup guide
- [ ] Authentication commands

**Prerequisites to document:**
1. GitHub account
2. GitHub CLI installed
3. SSH key generated and added to GitHub
4. GitHub CLI authenticated with SSH protocol
5. `delete_repo` scope granted

### For Developers

**What to provide:**
- [ ] Source code (`github_manager.py`)
- [ ] Icon assets (all formats)
- [ ] Build scripts (platform-specific)
- [ ] This AI builder guide
- [ ] README.md with full documentation

---

## 9. PLATFORM DIFFERENCES SUMMARY

| Aspect | macOS | Windows | Linux |
|--------|-------|---------|-------|
| **Package Format** | .app bundle | .exe executable | .desktop entry |
| **Icon Format** | .icns | .ico | .png |
| **GH Path** | `/opt/homebrew/bin/gh` | `C:\Program Files\GitHub CLI\gh.exe` | `/usr/bin/gh` |
| **Build Tool** | Manual bundle | PyInstaller | Manual install |
| **Install Location** | Applications or Desktop | Program Files | /usr/local/bin |
| **Menu Integration** | Automatic (drag to Apps) | Start Menu (installer) | .desktop file |
| **Path Separator** | `/` | `\\` (use raw strings) | `/` |

---

## 10. FINAL VERIFICATION SCRIPT

```bash
#!/bin/bash
# Run this to verify everything is set up correctly

echo "🔍 GitHub Repository Manager - Setup Verification"
echo "=================================================="

# 1. Check GitHub CLI
echo -n "GitHub CLI installed: "
if command -v gh &> /dev/null; then
    echo "✅ $(gh --version | head -n1)"
else
    echo "❌ Not found - install from https://cli.github.com/"
    exit 1
fi

# 2. Check authentication
echo -n "GitHub authentication: "
if gh auth status &> /dev/null; then
    echo "✅ Authenticated"
else
    echo "❌ Not authenticated - run: gh auth login"
    exit 1
fi

# 3. Check protocol
echo -n "Git protocol: "
PROTOCOL=$(gh config get git_protocol 2>/dev/null)
if [ "$PROTOCOL" = "ssh" ]; then
    echo "✅ SSH"
else
    echo "⚠️  $PROTOCOL - run: gh config set git_protocol ssh"
fi

# 4. Check delete_repo scope
echo -n "Delete permission: "
if gh auth status 2>&1 | grep -q "delete_repo"; then
    echo "✅ Granted"
else
    echo "❌ Missing - run: gh auth refresh -h github.com -s delete_repo"
    exit 1
fi

# 5. Check SSH
echo -n "SSH to GitHub: "
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ Working"
else
    echo "❌ Failed - check SSH key setup"
    exit 1
fi

# 6. Check Python
echo -n "Python 3: "
if command -v python3 &> /dev/null; then
    echo "✅ $(python3 --version)"
else
    echo "❌ Not found"
    exit 1
fi

# 7. Check Tkinter
echo -n "Tkinter: "
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ Available"
else
    echo "❌ Missing - install python3-tk"
    exit 1
fi

echo ""
echo "🎉 All checks passed! Ready to run GitHub Manager."
```

---

## 11. QUICK START FOR AI

If you're an AI recreating this on Windows/Linux, follow these steps in order:

1. **Get the logo** (GitHub Mark PNG from GitHub)
2. **Convert to platform icon** (.ico for Windows, .png for Linux)
3. **Install GitHub CLI** (platform package manager)
4. **Setup SSH** (generate key, add to GitHub, test)
5. **Authenticate GitHub CLI** (gh auth login, choose SSH)
6. **Grant delete permission** (gh auth refresh -s delete_repo)
7. **Find gh path** (which/where gh)
8. **Update GH_PATH in code** (line 14)
9. **Get username** (gh api user --jq .login)
10. **Update username in delete** (line 229)
11. **Test script directly** (python github_manager.py)
12. **Package for platform** (.exe, .app, or .desktop)
13. **Test packaged version**
14. **Verify all operations** (create, list, delete)

---

## 12. SUPPORT RESOURCES

- **GitHub CLI Docs:** https://cli.github.com/manual/
- **SSH Setup:** https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- **Tkinter Docs:** https://docs.python.org/3/library/tkinter.html
- **PyInstaller Docs:** https://pyinstaller.org/en/stable/
- **macOS .app Bundle:** https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html

---

**Good luck building! This guide contains everything needed for pixel-perfect recreation on any platform.** 🚀
