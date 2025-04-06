@echo off
echo Setting up CivitAI Telegram Feed...

:: Install dependencies
pip install -r "%~dp0requirements.txt"

:: Create the VBS script for silent execution
echo Set WinScriptHost = CreateObject("WScript.Shell") > "%~dp0run_caitgfeed.vbs"
echo WinScriptHost.Run "pythonw ""%~dp0main.py""", 0 >> "%~run_caitgfeed.vbs"
echo Set WinScriptHost = Nothing >> "%~run_caitgfeed.vbs"

echo Setup completed! You can now set up the Task Scheduler to run run_caitgfeed.vbs
pause