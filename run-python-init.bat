setlocal


REM --- Kill all Chrome processes
taskkill /F /IM chrome.exe >nul 2>&1

REM --- Launch the Python script
start "" /B cmd /c C:\Python311\python.exe -u "%USERPROFILE%\re_initialize\init.py" --chrome-data-dir "%chrome_data_dir%" --profile-directory "%chrome_default_profile%" >> "%USERPROFILE%\Documents\python_init_log.txt" 2>&1


endlocal
