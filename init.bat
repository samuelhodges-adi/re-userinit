@REM echo off

if "%1"=="chrome" (
  echo Launching Chrome
  call "%~dp0run-python-init.bat"
) else (
  echo Performing first time setup
  echo Copying user settings...

  robocopy "%programdata%\Remote Eval Agent\UserInit\AppData" "%appdata%\.." /E /COPYALL /R:2 /W:1
  robocopy "%programdata%\Remote Eval Agent\UserInit\UserProfile" "%userprofile%" /E /COPYALL /R:2 /W:1

  taskkill /F /IM ACE.exe
  timeout /t 8 /nobreak >nul

  start "" "C:\Program Files\Analog Devices\ACE\ACE.exe"
  call "%~dp0run-python-init.bat"
  timeout 10
)

exit /b
