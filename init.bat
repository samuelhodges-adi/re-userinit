@echo off
echo copying user settings
xcopy "%programdata%\Remote Eval Agent\UserInit\AppData\" "%appdata%\..\" /E/H/Y
xcopy "%programdata%\Remote Eval Agent\UserInit\UserProfile\" "%userprofile%\" /E/H/Y
timeout 8

start "" "C:\Program Files\Analog Devices\ACE\ACE.exe"
start "" C:\Python311\pythonw.exe "C:\ProgramData\Remote Eval Agent\init.py"

timeout 10

exit
