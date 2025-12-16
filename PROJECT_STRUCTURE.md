# Project Structure Guide

## Repository Contents

```
GIT_manager/
├── github_manager.py          # Main application (245 lines)
├── github_logo.png            # GitHub logo (source image)
├── github_logo.icns          # macOS icon (if built)
├── README.md                  # Complete documentation
├── AI_BUILDER_GUIDE.md       # Detailed guide for recreating on Windows/Linux
├── QUICKSTART.md             # Quick setup instructions
├── requirements.txt          # Python dependencies (none!)
├── LICENSE                   # MIT license
└── .gitignore               # Git ignore rules
```

## File Purposes

### `github_manager.py`
**The main application - works on all platforms**

**Key components:**
- Lines 1-14: Imports and configuration
- Line 14: `GH_PATH` - **MUST UPDATE FOR YOUR PLATFORM**
- Lines 16-30: GitHubManager class initialization
- Lines 32-89: UI creation (Tkinter)
- Lines 91-112: Load repositories from GitHub
- Lines 114-178: Create repository cards
- Lines 180-216: Create new repository
- Lines 218-258: Delete repository with permission handling

**Platform-specific changes needed:**
1. **Line 14** - Update `GH_PATH` to your `gh` location
2. **Line 229** - Replace `teadock` with your GitHub username

### `README.md`
**Complete user and developer documentation**

Contains:
- Feature list with emoji indicators
- Installation instructions for macOS, Windows, Linux
- Platform-specific setup (creating .app, .exe, .desktop)
- SSH setup guide
- GitHub CLI authentication
- Configuration details
- Usage instructions
- Troubleshooting
- Customization options
- AI builder quick reference

### `AI_BUILDER_GUIDE.md`
**Comprehensive guide for AI assistants**

**This is the most important file for recreating on other platforms!**

Contains:
- Critical requirements checklist
- Complete SSH setup (every command explained)
- GitHub CLI authentication (with troubleshooting)
- Platform-specific code modifications
- Packaging instructions (PyInstaller, .app bundle, .desktop)
- Testing checklist
- Common pitfalls and solutions
- Distribution checklist
- Platform differences table
- Final verification script

**Use this if you need to recreate the app on Windows or Linux.**

### `QUICKSTART.md`
**Fast setup for end users**

Step-by-step commands for:
- macOS users
- Windows users  
- Linux users

Copy-paste ready commands with minimal explanation.

### `github_logo.png`
**Source image for icons**

- Official GitHub Mark logo
- Transparent PNG
- Used to create platform-specific icons

**How to use:**
- **macOS**: Convert to .icns with multiple sizes
- **Windows**: Convert to .ico with multiple sizes
- **Linux**: Use as-is (.png) for desktop entry

### `requirements.txt`
**Python dependencies**

Actually empty! This app uses only standard library:
- `tkinter` - GUI (comes with Python on macOS/Windows)
- `subprocess` - Run `gh` commands
- `json` - Parse API responses
- `os` - Environment variables
- `datetime` - Format dates

**External dependency:**
- GitHub CLI (`gh`) - Must be installed separately

### `LICENSE`
**MIT License**

Allows anyone to:
- Use commercially
- Modify
- Distribute
- Sublicense

Only requirements:
- Include license in distributions
- Include copyright notice

### `.gitignore`
**Git ignore patterns**

Excludes:
- macOS system files (.DS_Store)
- Python bytecode (__pycache__)
- Build artifacts (dist/, build/)
- Virtual environments (venv/)
- IDE files (.vscode/, .idea/)
- Generated icons (*.icns, *.ico)

## Building for Different Platforms

### macOS - .app Bundle

**Structure:**
```
CreateGitHubRepo.app/
├── Contents/
│   ├── Info.plist              # App metadata
│   ├── MacOS/
│   │   └── CreateGitHubRepo    # Executable (github_manager.py)
│   └── Resources/
│       └── AppIcon.icns        # Icon (from github_logo.png)
```

**Steps:**
1. Create directory structure
2. Copy `github_manager.py` to `MacOS/CreateGitHubRepo`
3. Make executable: `chmod +x`
4. Create `Info.plist` with bundle info
5. Convert logo to .icns (multiple sizes)
6. Copy to `Resources/AppIcon.icns`

**Result:** Double-clickable app in Finder

### Windows - .exe Executable

**Build with PyInstaller:**
```bash
pyinstaller --onefile --windowed --icon=github_logo.ico --name="GitHub Manager" github_manager.py
```

**Output:**
```
dist/
└── GitHub Manager.exe    # Standalone executable
```

**Steps:**
1. Install PyInstaller: `pip install pyinstaller`
2. Convert logo to .ico (256x256 multi-size)
3. Run PyInstaller command
4. Distribute `dist/GitHub Manager.exe`

**Result:** Double-clickable .exe file

### Linux - Desktop Entry

**Installation locations:**
```
/usr/local/bin/github-manager          # Executable script
/usr/share/pixmaps/github-manager.png  # Icon
~/.local/share/applications/github-manager.desktop  # Menu entry
```

**Steps:**
1. Copy script to `/usr/local/bin/` and make executable
2. Copy icon to `/usr/share/pixmaps/`
3. Create `.desktop` file in `~/.local/share/applications/`
4. Update desktop database

**Result:** App appears in application menu

## Code Modification Checklist

When setting up on a new system:

- [ ] Find GitHub CLI path: `which gh` or `where gh`
- [ ] Update line 14: `GH_PATH = '/path/to/gh'`
- [ ] Get your username: `gh api user --jq .login`
- [ ] Update line 229: Replace `teadock` with your username
- [ ] Test: `python github_manager.py`
- [ ] Package for your platform (see above)

## Asset Conversion Reference

### PNG to ICNS (macOS)

**Method 1: Online converter**
- https://anyconv.com/png-to-icns-converter/
- Upload github_logo.png
- Download AppIcon.icns

**Method 2: Command line**
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

### PNG to ICO (Windows)

**Method 1: Online converter**
- https://convertio.co/png-ico/
- Upload github_logo.png
- Download github_logo.ico

**Method 2: ImageMagick**
```bash
convert github_logo.png -define icon:auto-resize=256,128,64,32,16 github_logo.ico
```

### PNG for Linux

No conversion needed - use `github_logo.png` directly!

## Distribution Checklist

Before sharing with others:

### For End Users
- [ ] Provide executable (.app, .exe, or install script)
- [ ] Include QUICKSTART.md
- [ ] List prerequisites (GitHub CLI, SSH setup)
- [ ] Provide setup commands
- [ ] Include troubleshooting section

### For Developers
- [ ] Provide source code (github_manager.py)
- [ ] Include all documentation (README, guides)
- [ ] Provide logo in all formats
- [ ] Include build scripts
- [ ] Add LICENSE file
- [ ] Create .gitignore

### For AI Builders
- [ ] AI_BUILDER_GUIDE.md is complete
- [ ] Platform-specific instructions included
- [ ] Common pitfalls documented
- [ ] Code modification points marked
- [ ] Testing checklist provided
- [ ] Verification script included

## Repository URL

**GitHub:** https://github.com/teadock/GIT_manager

Clone with:
```bash
# SSH (recommended)
git clone git@github.com:teadock/GIT_manager.git

# HTTPS
git clone https://github.com/teadock/GIT_manager.git
```

## Quick Commands

**Run directly:**
```bash
python3 github_manager.py
```

**Update gh path:**
```bash
# Find path
which gh  # macOS/Linux
where gh  # Windows

# Edit file
nano github_manager.py  # Change line 14
```

**Update username:**
```bash
# Get username
gh api user --jq .login

# Edit file
nano github_manager.py  # Change line 229
```

**Build for distribution:**
```bash
# macOS: See README.md "Platform-Specific Setup > macOS"
# Windows: pyinstaller --onefile --windowed --icon=github_logo.ico --name="GitHub Manager" github_manager.py
# Linux: See README.md "Platform-Specific Setup > Linux"
```

## Support

Questions? Issues? Enhancements?

1. Check `README.md` for detailed docs
2. Check `AI_BUILDER_GUIDE.md` for platform-specific help
3. Check `QUICKSTART.md` for setup commands
4. Open an issue on GitHub
5. Submit a pull request

---

**Everything you need to build, distribute, and maintain the GitHub Repository Manager is in this repository!** 🚀
