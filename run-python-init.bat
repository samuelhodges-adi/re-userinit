taskkill /F /IM chrome.exe
start "" /B cmd /c ""C:\Python311\python.exe" "%~dp0init.py" >> "%USERPROFILE%\Documents\python_init_log.txt" 2>&1
