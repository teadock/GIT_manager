# GitHub Manager - Windows Executable

## Quick Start

1. **Install GitHub CLI:**
   ```powershell
   winget install --id GitHub.cli
   ```

2. **Authenticate (select SSH protocol!):**
   ```powershell
   gh auth login
   ```

3. **Grant delete permission:**
   ```powershell
   gh auth refresh -h github.com -s delete_repo
   ```

4. **Run the app:**
   Double-click `GitHub-Manager.exe`

## Features

- Create private repositories
- List all repositories
- Delete repositories (with confirmation)
- No console window - clean GUI only

## Requirements

- Windows 10/11
- GitHub CLI installed and authenticated
- SSH protocol configured

**Note:** The executable includes Python runtime - no Python installation needed!


---

## ✨ What's Included

This is a **standalone Windows executable** that includes:
- ✅ Python runtime (no need to install Python!)
- ✅ All required libraries (tkinter, subprocess, etc.)
- ✅ Full GitHub Repository Manager functionality

---

## 🚀 Quick Start

### 1. Prerequisites
You only need **GitHub CLI** installed and authenticated:

```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Authenticate with SSH protocol
gh auth login
# Important: Select "SSH" when asked for git protocol!

# Grant delete permissions
gh auth refresh -h github.com -s delete_repo
```

### 2. Add Your SSH Key to GitHub
1. Go to: https://github.com/settings/ssh/new
2. Paste your public key from: `C:\Users\YourUsername\.ssh\id_ed25519.pub`
3. Click "Add SSH key"

### 3. Run the Application
**Just double-click:** `GitHub-Manager.exe`

That's it! No Python installation needed! 🎉

---

## 🎯 Features

### Create Repositories
- Enter repository name
- Click blue "Create New" button
- Repository created as private with SSH
- Name automatically copied to clipboard

### View Repositories
- All your repos displayed as cards
- Shows size, last push date, privacy status
- Sorted by most recently pushed
- Smooth mousewheel scrolling

### Delete Repositories
- Click red "Delete" button
- Confirmation dialog appears
- Click "Yes" to delete permanently
- **No additional authentication needed!**

---

## 📋 System Requirements

- **OS:** Windows 10 or Windows 11 (64-bit)
- **GitHub CLI:** Must be installed ([download here](https://cli.github.com/))
- **Authentication:** Must run `gh auth login` with SSH protocol
- **Permissions:** Must grant `delete_repo` scope
- **Internet:** Required for GitHub operations

---

## 🔧 First-Time Setup

If you're setting up for the first time:

### Step 1: Install GitHub CLI
```powershell
winget install --id GitHub.cli
```

### Step 2: Generate SSH Key (if you don't have one)
```powershell
ssh-keygen -t ed25519 -C "youremail@example.com"
# Press Enter for default location
# Enter passphrase or press Enter for no passphrase
```

### Step 3: Add SSH Key to GitHub
```powershell
# Copy your public key
type $env:USERPROFILE\.ssh\id_ed25519.pub | clip

# Then go to: https://github.com/settings/ssh/new
# Paste and save
```

### Step 4: Authenticate GitHub CLI
```powershell
gh auth login
```
**Important selections:**
- Account: GitHub.com
- Protocol: **SSH** ← Critical!
- Authenticate: Via web browser

### Step 5: Grant Delete Permissions
```powershell
gh auth refresh -h github.com -s delete_repo
```

### Step 6: Launch Application
Double-click `GitHub-Manager.exe`

---

## ✅ Verify Setup

Run this to check everything is configured:
```powershell
# Check GitHub CLI is installed
gh --version

# Check authentication
gh auth status

# Check SSH connection
ssh -T git@github.com
```

You should see:
- GitHub CLI version number
- "Logged in to github.com"
- Token scopes including `delete_repo`
- "Hi YourUsername! You've successfully authenticated..."

---

## ⚠️ Troubleshooting

### "gh: command not found" or application doesn't work
- GitHub CLI is not installed or not in PATH
- **Solution:** Install GitHub CLI and restart your computer

### Can't delete repositories
- Missing `delete_repo` scope
- **Solution:** Run `gh auth refresh -h github.com -s delete_repo`

### "Permission denied (publickey)"
- SSH key not added to GitHub
- **Solution:** Add your SSH key at https://github.com/settings/ssh/new

### Application window appears but list is empty
- Not authenticated with GitHub CLI
- **Solution:** Run `gh auth login` and select SSH protocol

### Application won't start
- Antivirus might be blocking it
- **Solution:** Add exception for GitHub-Manager.exe

---

## 🔐 Security

### What This Application Can Do
- ✅ Create private repositories on your GitHub account
- ✅ List your repositories
- ✅ Delete your repositories (with confirmation)

### What This Application CANNOT Do
- ❌ Access repositories you don't own
- ❌ Perform actions without confirmation dialogs
- ❌ Store your credentials (uses GitHub CLI authentication)

### Your Data
- All operations go through GitHub's official API
- Authentication is handled by GitHub CLI
- No data is stored or transmitted elsewhere
- All repositories created are private by default

---

## 📁 File Locations

### Application
- **Executable:** `dist\GitHub-Manager.exe`
- **Size:** 10.66 MB

### Configuration Files (created by GitHub CLI)
- **GitHub Config:** `C:\Users\YourUsername\.gitconfig`
- **SSH Keys:** `C:\Users\YourUsername\.ssh\`
- **GitHub CLI Config:** `C:\Users\YourUsername\AppData\Roaming\GitHub CLI\`

---

## 💡 Tips

### Creating Repositories
- ✅ Use letters, numbers, hyphens, underscores only
- ✅ Name is copied to clipboard automatically
- ✅ All repos are created as **private** by default
- ✅ **SSH** protocol is used automatically

### Deleting Repositories
- ⚠️ Always shows confirmation dialog
- ⚠️ Deletion is **permanent** and cannot be undone
- ⚠️ Deletes all code, issues, pull requests, and history
- ✅ Executes immediately after confirmation

### Performance
- Fast repository listing (caches results)
- Smooth scrolling through large repository lists
- Instant clipboard copy after creation

---

## 🆚 Executable vs Python Script

### Use the `.exe` if:
- ✅ You don't have Python installed
- ✅ You want a double-click experience
- ✅ You prefer a standalone application

### Use the Python script (`github_manager.py`) if:
- ✅ You have Python installed
- ✅ You want to modify the code
- ✅ You want the latest features
- ✅ You need to use it on macOS/Linux too

**Both have identical functionality!**

---

## 📞 Support

### Common Issues
1. **Application won't start:** Restart computer after installing GitHub CLI
2. **Can't see repositories:** Run `gh auth login`
3. **Can't delete:** Run `gh auth refresh -h github.com -s delete_repo`
4. **Errors about SSH:** Add SSH key to GitHub

### Testing Your Setup
A test script is included: `test_auth.py`
```powershell
python test_auth.py
```

This will verify:
- GitHub CLI installation
- Authentication status
- Repository access
- Delete permissions

---

## 🎊 Ready to Use!

Once you've completed the first-time setup:
1. **Double-click** `GitHub-Manager.exe`
2. **Create** repositories with one click
3. **Delete** repositories with one click (+ confirmation)
4. **Enjoy** a beautiful, native GitHub management experience!

---

**Version:** 1.0  
**Built:** December 16, 2025  
**Platform:** Windows 10/11 (64-bit)  
**Author:** teadock  
**License:** MIT
