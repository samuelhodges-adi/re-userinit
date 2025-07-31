@REM echo off

if "%1"=="chrome" (
  @echo off
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
  echo Overwriting AppData...
  robocopy "C:\ProgramData\Remote Eval Agent\UserInit\AppData" "%userprofile%\AppData" /E /COPY:DAT /IS /R:1 /W:1 /MT:8 /NP

  echo Overwriting entire user profile...
  robocopy "C:\ProgramData\Remote Eval Agent\UserInit\UserProfile" "%userprofile%" /E /COPY:DAT /IS /R:1 /W:1 /MT:8 /NP

  echo Restarting ACE...
  taskkill /F /IM ACE.exe
  timeout 8

  start "" "C:\Program Files\Analog Devices\ACE (Apollo)\ACE.exe"

  REM --- Set up variables
  if not defined chrome_original_data_dir set "chrome_original_data_dir=%USERPROFILE%\AppData\Local\Google\Chrome\User Data"
  if not defined chrome_data_dir set "chrome_data_dir=%USERPROFILE%\AppData\Local\Google\Chrome\User Data Copy"

  REM --- If the copy profile doesn't exist, copy original to copy location
  if not exist "%chrome_data_dir%" (
      REM --- Kill all Chrome processes
      taskkill /F /IM chrome.exe >nul 2>&1

      echo Creating Chrome profile copy...
      xcopy /e /i /h /y "%chrome_original_data_dir%" "%chrome_data_dir%"
  )

  call "%~dp0run-python-init.bat"
  timeout 10
)

exit /b

