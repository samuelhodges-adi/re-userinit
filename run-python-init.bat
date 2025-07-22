taskkill /F /IM chrome.exe
start "" /B cmd /c C:\Python311\python.exe -u "%USERPROFILE%\re_initialize\init.py" >> "%USERPROFILE%\Documents\python_init_log.txt" 2>&1
