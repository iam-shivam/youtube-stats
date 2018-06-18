@echo off
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "%cd%\SupportFiles\addToPath.ps1" "%cd%\Drivers" ' -Verb RunAs}"
python %cd%/SupportFiles/youtubeStats.py