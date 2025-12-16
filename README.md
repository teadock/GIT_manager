# GitHub Repository Manager

A beautiful, native desktop application for managing GitHub repositories with create, list, and delete functionality - all without leaving your desktop.

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

✨ **Beautiful Native UI** - macOS-style design with card-based repository list  
🚀 **Quick Repository Creation** - Create private repos with one click  
🗑️ **Safe Deletion** - Delete repositories with confirmation dialog  
📋 **Clipboard Integration** - Auto-copy new repo names  
🔄 **Auto-Refresh** - List updates automatically after changes  
📅 **Smart Sorting** - Repositories sorted by last push date  
🔐 **SSH Protocol** - All repos created with SSH URLs  
📦 **Size Display** - Shows repository disk usage  
🔒 **Privacy Indicators** - Clear private/public status  

## Screenshots

### macOS Version
- Card-based repository list
- Blue "Create New" button
- Red "Delete" buttons with confirmation
- Clean, modern design matching macOS UI guidelines

## Quick Start

### Prerequisites
- Python 3.8 or higher
- GitHub CLI (`gh`) installed and authenticated
- Tkinter (usually comes with Python)

### Installation

1. **Clone this repository:**
   ```bash
   git clone git@github.com:teadock/GIT_manager.git
   cd GIT_manager
   ```

2. **Install GitHub CLI** (if not already installed):
   
   **macOS:**
   ```bash
   brew install gh
   ```
   
   **Windows:**
   ```powershell
   winget install GitHub.cli
   ```
   
   **Linux:**
   ```bash
   # Debian/Ubuntu
   sudo apt install gh
   
   # Fedora
   sudo dnf install gh
   ```

3. **Authenticate with GitHub:**
   ```bash
   gh auth login
   ```
   Choose:
   - GitHub.com
   - SSH protocol
   - Login via browser

4. **Grant delete permissions:**
   ```bash
   gh auth refresh -h github.com -s delete_repo
   ```

5. **Run the application:**
   ```bash
   python github_manager.py
   ```

## Platform-Specific Setup

### macOS

#### Creating .app Bundle

1. **Create directory structure:**
   ```bash
   mkdir -p ~/Desktop/CreateGitHubRepo.app/Contents/{MacOS,Resources}
   ```

2. **Copy Python script:**
   ```bash
   cp github_manager.py ~/Desktop/CreateGitHubRepo.app/Contents/MacOS/CreateGitHubRepo
   chmod +x ~/Desktop/CreateGitHubRepo.app/Contents/MacOS/CreateGitHubRepo
   ```

3. **Create Info.plist:**
   ```bash
   cat > ~/Desktop/CreateGitHubRepo.app/Contents/Info.plist << 'EOF'
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>CFBundleExecutable</key>
       <string>CreateGitHubRepo</string>
       <key>CFBundleIconFile</key>
       <string>AppIcon</string>
       <key>CFBundleIdentifier</key>
       <string>com.teadock.creategithubrepo</string>
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
   ```

4. **Add icon (optional):**
   - Download GitHub logo PNG
   - Convert to .icns using online tool or: `sips -s format icns github_logo.png --out AppIcon.icns`
   - Copy to: `~/Desktop/CreateGitHubRepo.app/Contents/Resources/AppIcon.icns`

### Windows

#### Creating .exe with PyInstaller

1. **Install PyInstaller:**
   ```powershell
   pip install pyinstaller
   ```

2. **Create icon (optional):**
   - Download GitHub logo PNG
   - Convert to .ico format (256x256)
   - Save as `github_logo.ico`

3. **Build executable:**
   ```powershell
   pyinstaller --onefile --windowed --icon=github_logo.ico --name="GitHub Manager" github_manager.py
   ```

4. **Update GH_PATH in code:**
   - Find GitHub CLI location: `where gh`
   - Update line 14 in `github_manager.py`:
     ```python
     GH_PATH = r'C:\Program Files\GitHub CLI\gh.exe'  # Your actual path
     ```

5. **Create desktop shortcut:**
   - Right-click `dist/GitHub Manager.exe`
   - Send to → Desktop (create shortcut)

### Linux

#### Creating Desktop Entry

1. **Copy script to bin:**
   ```bash
   sudo cp github_manager.py /usr/local/bin/github-manager
   sudo chmod +x /usr/local/bin/github-manager
   ```

2. **Create desktop entry:**
   ```bash
   cat > ~/.local/share/applications/github-manager.desktop << 'EOF'
   [Desktop Entry]
   Name=GitHub Manager
   Comment=Manage GitHub repositories
   Exec=/usr/local/bin/github-manager
   Icon=github
   Terminal=false
   Type=Application
   Categories=Development;
   EOF
   ```

3. **Update GH_PATH in code:**
   ```bash
   which gh  # Find gh location
   # Update line 14 to match
   ```

## Configuration

### GitHub CLI Path

The app needs to know where the `gh` command is located. Update line 14 in `github_manager.py`:

**macOS (Homebrew):**
```python
GH_PATH = '/opt/homebrew/bin/gh'
```

**Windows:**
```python
GH_PATH = r'C:\Program Files\GitHub CLI\gh.exe'
```

**Linux:**
```python
GH_PATH = '/usr/bin/gh'
```

### Username

Update line 229 to use your GitHub username:
```python
[GH_PATH, 'repo', 'delete', f'YOUR_USERNAME/{name}', '--yes']
```

## Usage

### Creating a Repository

1. Type repository name in text field
2. Click "Create New" (or press Enter)
3. Repository created as private with SSH URL
4. Name automatically copied to clipboard
5. List refreshes to show new repo

### Deleting a Repository

1. Click red "Delete" button on any repository card
2. Confirm deletion in dialog
3. Repository permanently deleted from GitHub
4. List refreshes automatically

### Keyboard Shortcuts

- **Enter** - Create repository (when text field focused)
- **Mouse wheel** - Scroll repository list

## Architecture

### Core Components

```
github_manager.py
├── GitHubManager (main class)
│   ├── __init__() - Initialize window and UI
│   ├── create_ui() - Build interface
│   ├── load_repositories() - Fetch repo list from GitHub
│   ├── create_repo_item() - Render repository card
│   ├── create_repository() - Handle repo creation
│   └── delete_repository() - Handle repo deletion
└── main - Create Tk window and run app
```

### GitHub CLI Integration

All GitHub operations use the `gh` CLI tool:

- **List repos:** `gh repo list --limit 100 --json name,diskUsage,pushedAt,isPrivate`
- **Create repo:** `gh repo create <name> --private`
- **Delete repo:** `gh repo delete <owner>/<name> --yes`

### Data Flow

```
User Action → Tkinter Event → GitHub CLI Command → JSON Response → UI Update
```

## SSH Setup Guide

### Why SSH?

SSH authentication eliminates password prompts and is more secure than HTTPS.

### Complete SSH Setup

1. **Check for existing SSH keys:**
   ```bash
   ls -la ~/.ssh/id_*.pub
   ```

2. **Generate new SSH key (if needed):**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   - Press Enter for default location
   - Set passphrase (or leave empty)

3. **Start SSH agent:**
   ```bash
   eval "$(ssh-agent -s)"
   ```

4. **Add key to SSH agent:**
   
   **macOS:**
   ```bash
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   ```
   
   **Windows/Linux:**
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

5. **Copy public key:**
   
   **macOS:**
   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```
   
   **Windows:**
   ```powershell
   type ~/.ssh/id_ed25519.pub | clip
   ```
   
   **Linux:**
   ```bash
   cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard
   ```

6. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste public key
   - Click "Add SSH key"

7. **Test connection:**
   ```bash
   ssh -T git@github.com
   ```
   Should see: "Hi username! You've successfully authenticated..."

8. **Configure GitHub CLI to use SSH:**
   ```bash
   gh auth login
   ```
   - Select: GitHub.com
   - Choose: SSH
   - Follow prompts

## GitHub CLI Authentication

### Initial Setup

```bash
gh auth login
```

Follow prompts:
1. **Account:** GitHub.com
2. **Protocol:** SSH
3. **SSH key:** Select your key or upload new one
4. **Authentication:** Login with browser

### Required Scopes

The app needs the `delete_repo` scope to delete repositories:

```bash
gh auth refresh -h github.com -s delete_repo
```

This opens your browser for one-time authentication.

### Verify Authentication

```bash
gh auth status
```

Should show:
```
✓ Logged in to github.com account USERNAME (keyring)
- Token scopes: 'admin:public_key', 'gist', 'read:org', 'repo', 'delete_repo'
```

## Troubleshooting

### "gh: command not found"

**Fix:** Install GitHub CLI:
- macOS: `brew install gh`
- Windows: `winget install GitHub.cli`
- Linux: See official docs for your distro

### "Permission Required - delete_repo scope"

**Fix:** Grant deletion permission:
```bash
gh auth refresh -h github.com -s delete_repo
```

### App won't open on macOS

**Fix:** Make executable:
```bash
chmod +x ~/Desktop/CreateGitHubRepo.app/Contents/MacOS/CreateGitHubRepo
```

### "Failed to load repositories"

**Fix:** Check GitHub CLI is authenticated:
```bash
gh auth status
gh auth login  # If not authenticated
```

### Wrong PATH to gh command

**Fix:** Find correct path:
```bash
which gh  # macOS/Linux
where gh  # Windows
```

Update `GH_PATH` in code.

### Repository created but with HTTPS URL

**Fix:** Reconfigure GitHub CLI:
```bash
gh config set git_protocol ssh
```

### "Repository name can only contain..."

Repository names must:
- Contain only letters, numbers, hyphens, underscores
- Not start with hyphen
- Not contain spaces or special characters

## Customization

### Colors

Edit lines 23-27 to change color scheme:
```python
self.bg_color = '#f5f5f7'      # Background
self.button_color = '#007AFF'   # Create button (blue)
self.delete_color = '#FF3B30'   # Delete button (red)
self.item_bg = '#FFFFFF'        # Card background
```

### Window Size

Edit line 21:
```python
self.root.geometry("700x600")  # Width x Height
```

### Font

Edit font family in lines 38, 48, etc:
```python
font=('SF Pro Text', 14)  # macOS
font=('Segoe UI', 14)     # Windows
font=('Ubuntu', 14)        # Linux
```

### Repository Limit

Edit line 98 to show more/fewer repos:
```python
[GH_PATH, 'repo', 'list', '--limit', '100', ...]
```

## Building Guide for AI

### Complete Recreation Steps

If you're an AI recreating this project on Windows or Linux:

#### 1. **Assets Required**
- GitHub logo (PNG or SVG)
- Convert to platform icon format:
  - Windows: .ico (256x256)
  - macOS: .icns (multiple sizes)
  - Linux: .png (128x128 or 256x256)

#### 2. **SSH Configuration**
```bash
# Generate key
ssh-keygen -t ed25519 -C "email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# → Paste at github.com/settings/keys

# Test
ssh -T git@github.com
```

#### 3. **GitHub CLI Setup**
```bash
# Install gh (platform-specific)
# Then:
gh auth login
# Choose: GitHub.com → SSH → Browser login

# Grant deletion permission
gh auth refresh -h github.com -s delete_repo
```

#### 4. **Code Modifications**

**Find gh path:**
```bash
which gh      # macOS/Linux
where gh      # Windows
```

**Update line 14:**
```python
GH_PATH = '/path/to/gh'  # Use actual path
```

**Update line 229 (your username):**
```python
[GH_PATH, 'repo', 'delete', f'USERNAME/{name}', '--yes']
```

#### 5. **Platform-Specific Packaging**

**Windows (.exe):**
```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --icon=github_logo.ico --name="GitHub Manager" github_manager.py
```

**macOS (.app):**
```bash
# Create bundle structure
mkdir -p GitHubManager.app/Contents/{MacOS,Resources}

# Copy script
cp github_manager.py GitHubManager.app/Contents/MacOS/GitHubManager
chmod +x GitHubManager.app/Contents/MacOS/GitHubManager

# Create Info.plist (see macOS section above)

# Add icon
cp github_logo.icns GitHubManager.app/Contents/Resources/AppIcon.icns
```

**Linux (.desktop):**
```bash
# Install to system
sudo cp github_manager.py /usr/local/bin/github-manager
sudo chmod +x /usr/local/bin/github-manager

# Create desktop entry (see Linux section above)
```

#### 6. **Testing Checklist**

- [ ] App launches without errors
- [ ] Repository list loads
- [ ] Repositories sorted by date (newest first)
- [ ] "Create New" creates private repo
- [ ] New repo name copied to clipboard
- [ ] List refreshes after creation
- [ ] Delete shows confirmation dialog
- [ ] Delete removes repo from GitHub
- [ ] List refreshes after deletion
- [ ] SSH URLs used (not HTTPS)
- [ ] Error messages are clear and helpful

#### 7. **Common Pitfalls**

⚠️ **PATH issues** - App bundle doesn't inherit shell PATH  
✅ Solution: Use absolute path to `gh` command

⚠️ **Wrong protocol** - Repos created with HTTPS instead of SSH  
✅ Solution: `gh config set git_protocol ssh`

⚠️ **Missing scope** - Can't delete repos  
✅ Solution: `gh auth refresh -h github.com -s delete_repo`

⚠️ **Username hardcoded** - Delete fails for other users  
✅ Solution: Update line 229 with actual username

⚠️ **Tkinter not found** - Python missing GUI support  
✅ Solution: Install `python-tk` package

## Advanced Features

### Future Enhancements

Potential improvements for contributors:

- [ ] **Repository search/filter** - Search by name
- [ ] **Bulk operations** - Select multiple repos
- [ ] **Clone button** - Clone repos to local machine
- [ ] **Open in browser** - Quick link to repo on GitHub
- [ ] **Visibility toggle** - Change public/private status
- [ ] **Description editing** - Update repo descriptions
- [ ] **Topic management** - Add/remove repository topics
- [ ] **Star/unstar** - Manage starred repositories
- [ ] **Multi-account** - Switch between GitHub accounts
- [ ] **Theme support** - Dark/light mode toggle
- [ ] **Repo templates** - Create from templates
- [ ] **Settings panel** - Configure app preferences

## License

MIT License - feel free to use and modify!

## Credits

Created with ❤️ for seamless GitHub repository management.

Built with:
- Python 3
- Tkinter (GUI)
- GitHub CLI (API integration)

## Support

Issues? Questions? Feature requests?

Open an issue on GitHub or submit a pull request!

---

**Pro Tip:** Add this to your dock/taskbar for instant GitHub repository management! 🚀
