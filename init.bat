@REM echo off

if "%1"=="chrome" (
  echo Launching Chrome
  call "%~dp0run-python-init.bat"
) else (
  echo Performing first time setup
  echo copying user settings
  xcopy "%programdata%\Remote Eval Agent\UserInit\AppData\" "%appdata%\..\" /E/H/Y
  xcopy "%programdata%\Remote Eval Agent\UserInit\UserProfile\" "%userprofile%\" /E/H/Y

  taskkill /F /IM ACE.exe
  timeout 8

  start "" "C:\Program Files\Analog Devices\ACE\ACE.exe"
  call "%~dp0run-python-init.bat"
  timeout 10
)

exit /b
