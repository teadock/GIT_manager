# GitHub Repository Manager# GitHub Repository Manager



A desktop application for managing GitHub repositories - create, list, and delete with a single click.A desktop application for managing GitHub repositories - create, list, and delete with a single click.



![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue)![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue)

![Python](https://img.shields.io/badge/python-3.8%2B-green)![Python](https://img.shields.io/badge/python-3.8%2B-green)

![License](https://img.shields.io/badge/license-MIT-blue)![License](https://img.shields.io/badge/license-MIT-blue)



## Features## Features



- ✅ Create private repositories instantly- ✅ Create private repositories instantly

- ✅ List all repositories with size, date, and privacy status- ✅ List all repositories with size, date, and privacy status

- ✅ Delete repositories with confirmation (no extra auth needed)- ✅ Delete repositories with confirmation (no extra auth needed)

- ✅ Auto-copy repository names to clipboard- ✅ Auto-copy repository names to clipboard

- ✅ Cross-platform (Windows, macOS, Linux)- ✅ Cross-platform (Windows, macOS, Linux)

- ✅ Beautiful macOS-style UI

## Installation & Setup

## Installation & Setup

### 1. Install GitHub CLI

### 1. Install GitHub CLI

**Windows:**

**Windows:**```powershell

```powershellwinget install --id GitHub.cli

winget install --id GitHub.cli```

```

**macOS:**

**macOS:**```bash

```bashbrew install gh

brew install gh```

```

**Linux:**

**Linux:**```bash

```bash# Debian/Ubuntu

# Debian/Ubuntusudo apt install gh

sudo apt install gh

# Fedora

# Fedorasudo dnf install gh

sudo dnf install gh```

```

### 2. Authenticate with GitHub

### 2. Authenticate with GitHub

**Important:** Select **SSH protocol** when prompted!

**Important:** Select **SSH protocol** when prompted!

```bash

```bashgh auth login

gh auth login```

```

Choose:

Choose:- GitHub.com

- GitHub.com- **SSH protocol** ← Important!

- **SSH protocol** ← Important!- Login via browser

- Login via browser

### 3. Grant Delete Permission

### 3. Grant Delete Permission

This allows the app to delete repositories without additional authentication:

This allows the app to delete repositories without additional authentication:

```bash

```bashgh auth refresh -h github.com -s delete_repo

gh auth refresh -h github.com -s delete_repo```

```

### 4. Run the Application

### 4. Run the Application

**Using Python:**

**Using Python:**```bash

```bashpython github_manager.py

python github_manager.py```

```

**Using Windows Executable:**

**Using Windows Executable:**```

```Double-click: dist\GitHub-Manager.exe

Double-click: dist\GitHub-Manager.exe```

```

**Using Windows Launcher:**

**Using Windows Launcher:**```

```Double-click: launch.bat

Double-click: launch.bat```

```

## Usage

## Usage

1. **Create Repository:** Enter name, click "Create New" (creates private repo with SSH)

1. **Create Repository:** Enter name, click "Create New" (creates private repo with SSH)2. **View Repositories:** Scroll through your repos with size, date, and privacy info

2. **View Repositories:** Scroll through your repos with size, date, and privacy info3. **Delete Repository:** Click red "Delete" button, confirm deletion

3. **Delete Repository:** Click red "Delete" button, confirm deletion

## Requirements

## Requirements

- Python 3.8+ (not needed for Windows .exe)

- Python 3.8+ (not needed for Windows .exe)- GitHub CLI (`gh`) - authenticated with SSH

- GitHub CLI (`gh`) - authenticated with SSH- Delete permission scope (`delete_repo`)

- Delete permission scope (`delete_repo`)

## Project Structure

## Project Structure

```

```GIT_manager/

GIT_manager/├── github_manager.py      # Main application

├── github_manager.py      # Main application├── github_manager.ico     # Application icon

├── github_manager.ico     # Application icon├── dist/

├── github_logo.png        # GitHub Octocat logo│   └── GitHub-Manager.exe # Windows executable

├── dist/├── launch.bat             # Windows launcher

│   ├── GitHub-Manager.exe # Windows executable├── test_auth.py          # Authentication tester

│   └── README.txt         # Executable instructions└── README.md             # This file

├── launch.bat             # Windows launcher       <string>1</string>

├── test_auth.py          # Authentication tester   </dict>

├── requirements.txt       # Dependencies (none!)   </plist>

└── README.md             # This file   EOF

```   ```



## Testing Authentication4. **Add icon (optional):**

   - Download GitHub logo PNG

Run the included test script to verify your setup:   - Convert to .icns using online tool or: `sips -s format icns github_logo.png --out AppIcon.icns`

   - Copy to: `~/Desktop/CreateGitHubRepo.app/Contents/Resources/AppIcon.icns`

```bash

python test_auth.py### Windows

```

#### Creating .exe with PyInstaller

This will check:

- GitHub CLI installation1. **Install PyInstaller:**

- Authentication status   ```powershell

- Repository access   pip install pyinstaller

- Delete permissions   ```



## License2. **Create icon (optional):**

   - Download GitHub logo PNG

MIT License - see LICENSE file for details   - Convert to .ico format (256x256)

   - Save as `github_logo.ico`

## Author

3. **Build executable:**

Created for easy GitHub repository management with a beautiful, native UI.   ```powershell

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
