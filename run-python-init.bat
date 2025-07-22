setlocal


REM --- Kill all Chrome processes
taskkill /F /IM chrome.exe >nul 2>&1


REM --- Set up variables
if not defined chrome_original_data_dir set "chrome_original_data_dir=%USERPROFILE%\AppData\Local\Google\Chrome\User Data"
if not defined chrome_data_dir set "chrome_data_dir=%USERPROFILE%\AppData\Local\Google\Chrome\User Data Copy"
if not defined chrome_default_profile set "chrome_default_profile=Default"


REM --- If the copy profile doesn't exist, copy original to copy location
if not exist "%chrome_data_dir%" (
    echo Creating Chrome profile copy...
    xcopy /e /i /h /y "%chrome_original_data_dir%" "%chrome_data_dir%"
)


REM --- Launch the Python script
start "" /B cmd /c C:\Python311\python.exe -u "%USERPROFILE%\re_initialize\init.py" --chrome-data-dir "%chrome_data_dir%" --profile-directory "%chrome_default_profile%" >> "%USERPROFILE%\Documents\python_init_log.txt" 2>&1


endlocal
