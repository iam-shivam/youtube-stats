@echo off
set /p download="Do you have python-3 installed? (y/n): "
echo .
if "%download%"=="n" GOTO downloadRequired
if "%download%"=="N" GOTO downloadRequired
GOTO noDownload

:downloadRequired
Powershell.exe -executionpolicy remotesigned -File "%cd%\SupportFiles\downloader.ps1"
echo "Installing Python..."
%cd%\SupportFiles\python-3.6.5.exe /quiet InstallAllUsers=1 PrependPath=1
echo "Installation Completed."

:noDownload
REM Powershell.exe -executionpolicy remotesigned -File "%cd%\SupportFiles\addToPath.ps1" "%cd%\Drivers"
REM PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "%cd%\SupportFiles\addToPath.ps1" "%cd%\Drivers" ' -Verb RunAs}"

echo "Adding Dependencies."
%cd%\SupportFiles\add-dependencies.bat
