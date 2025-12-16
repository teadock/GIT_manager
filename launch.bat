@echo off
REM GitHub Repository Manager Launcher
REM This ensures the GitHub CLI is in the PATH

REM Refresh PATH from registry
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
set "PATH=%SYS_PATH%;%USER_PATH%"

REM Launch the application
python "%~dp0github_manager.py"

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Error launching application. Press any key to exit...
    pause >nul
)
