@REM echo off

if "%1"=="chrome" (
  echo Launching Chrome
  call "%~dp0run-python-init.bat"
) else (
  echo Performing first time setup  
  echo Deleting existing user Desktop and Chrome data...

  if exist "%userprofile%\Desktop" (
    rmdir /S /Q "%userprofile%\Desktop"
  )

  if exist "%localappdata%\Google\Chrome" (
    rmdir /S /Q "%localappdata%\Google\Chrome"
  )

  echo Copying user settings...

  rem Only copy Data, Attributes, and Timestamps — no security, no ownership
  robocopy "C:\ProgramData\Remote Eval Agent\UserInit\AppData" "%appdata%\.." /E /COPY:DAT /R:1 /W:1 /MT:8 /NJH /NJS /NFL /NDL /NP
  robocopy "C:\ProgramData\Remote Eval Agent\UserInit\UserProfile" "%userprofile%" /E /COPY:DAT /R:1 /W:1 /MT:8 /NJH /NJS /NFL /NDL /NP

  taskkill /F /IM ACE.exe
  timeout 8

  start "" "C:\Program Files\Analog Devices\ACE\ACE.exe"
  call "%~dp0run-python-init.bat"
  timeout 10
)

exit /b
