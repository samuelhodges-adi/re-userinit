@REM echo off

if "%1"=="chrome" (
  echo Launching Chrome
  call "%~dp0run-python-init.bat"
) else (
  echo Performing first time setup  
  echo Deleting existing user Desktop and Chrome data...

  rmdir /S /Q "%userprofile%\Desktop"
  rmdir /S /Q "%localappdata%\Google\Chrome"

  echo Copying user settings...  
  
  robocopy "C:\ProgramData\Remote Eval Agent\UserInit\AppData" "%appdata%\.." /E /COPY:DATSO /R:2 /W:1  
  robocopy "C:\ProgramData\Remote Eval Agent\UserInit\UserProfile" "%userprofile%" /E /COPY:DATSO /R:2 /W:1  
  
  taskkill /F /IM ACE.exe  
  timeout /t 8 /nobreak >nul

  start "" "C:\Program Files\Analog Devices\ACE\ACE.exe"  
  call "%~dp0run-python-init.bat"  
  timeout /t 10 /nobreak >nul
)

exit /b

