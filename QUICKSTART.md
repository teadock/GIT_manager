# Quick Setup Guide

## For macOS Users

### 1. Install GitHub CLI
```bash
brew install gh
```

### 2. Setup SSH Key
```bash
# Generate key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add to agent
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Copy public key
pbcopy < ~/.ssh/id_ed25519.pub
```

### 3. Add SSH Key to GitHub
1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

### 4. Authenticate GitHub CLI
```bash
gh auth login
```
- Choose: GitHub.com
- Choose: SSH
- Login via browser

### 5. Grant Delete Permission
```bash
gh auth refresh -h github.com -s delete_repo
```

### 6. Run the App
```bash
python3 github_manager.py
```

## For Windows Users

### 1. Install GitHub CLI
```powershell
winget install GitHub.cli
```

### 2. Setup SSH Key
```bash
# In Git Bash or PowerShell
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent (PowerShell)
Start-Service ssh-agent

# Add to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key (PowerShell)
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
```

### 3. Add SSH Key to GitHub
Same as macOS (step 3)

### 4. Authenticate GitHub CLI
```bash
gh auth login
```
- Choose: GitHub.com
- Choose: SSH
- Login via browser

### 5. Grant Delete Permission
```bash
gh auth refresh -h github.com -s delete_repo
```

### 6. Update Code
1. Find GitHub CLI path: `where gh`
2. Edit `github_manager.py` line 14:
   ```python
   GH_PATH = r'C:\Program Files\GitHub CLI\gh.exe'
   ```
3. Edit line 229 with your username:
   ```python
   [GH_PATH, 'repo', 'delete', f'YOUR_USERNAME/{name}', '--yes']
   ```

### 7. Run or Build
**Run directly:**
```bash
python github_manager.py
```

**Build .exe:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="GitHub Manager" github_manager.py
```

## For Linux Users

### 1. Install GitHub CLI
**Ubuntu/Debian:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Fedora:**
```bash
sudo dnf install gh
```

### 2. Install Tkinter
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### 3. Setup SSH Key
```bash
# Generate key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Then copy manually or use xclip:
# sudo apt install xclip
# cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard
```

### 4-5. GitHub Setup
Same as macOS (steps 3-5)

### 6. Update Code
1. Find GitHub CLI path: `which gh`
2. Edit `github_manager.py` line 14:
   ```python
   GH_PATH = '/usr/bin/gh'
   ```
3. Edit line 229 with your username

### 7. Run the App
```bash
python3 github_manager.py
```

## Verification

After setup, verify everything works:

```bash
# Check GitHub CLI
gh --version

# Check authentication
gh auth status

# Should show:
# ✓ Logged in to github.com
# - Token scopes: ... 'delete_repo' ...
# - Git operations protocol: ssh

# Check SSH
ssh -T git@github.com

# Should show:
# Hi USERNAME! You've successfully authenticated...
```

## Usage

1. **Create Repository:**
   - Type name in text field
   - Click "Create New" or press Enter
   - Repository created and name copied to clipboard

2. **Delete Repository:**
   - Click red "Delete" button
   - Confirm deletion
   - Repository permanently deleted

3. **View Repositories:**
   - Automatically loads on startup
   - Sorted by last push date (newest first)
   - Shows name, size, date, privacy status

## Troubleshooting

**"gh: command not found"**
→ Install GitHub CLI (see step 1 above)

**"Permission Required - delete_repo scope"**
→ Run: `gh auth refresh -h github.com -s delete_repo`

**"Repository created with HTTPS"**
→ Run: `gh config set git_protocol ssh`

**"ModuleNotFoundError: tkinter"**
→ Install python3-tk (Linux only, see step 2)

**App won't start on macOS**
→ Run: `chmod +x github_manager.py`

## Support

For detailed instructions, see:
- `README.md` - Complete documentation
- `AI_BUILDER_GUIDE.md` - Platform-specific building guide

Issues? Open an issue on GitHub!
