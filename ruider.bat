@echo off
SETLOCAL enabledelayedexpansion

REM Define the path to the launcher script
SET SCRIPT=%~dp0\launcher.py

REM Default Python executable to pythonw.exe
set "PYTHON_EXE=pythonw.exe"

REM Loop through all command-line arguments
for %%A in (%*) do (
    REM Extract the first character of each argument
    set item=%%A
    set firstchar=!item:~0,1!
    REM Check if the first character is a dash
    if "!firstchar!" == "-" (
        REM Set Python executable to python.exe and exit the loop
        set "PYTHON_EXE=python.exe"
        goto runscript
    )
)

:runscript
REM Run launcher.py with the determined Python executable
if "%PYTHON_EXE%" == "pythonw.exe" (
    REM Use start command to attempt to suppress the console window
    start "" pythonw "%SCRIPT%" %*
) else (
    REM Run python script with console window
    python "%SCRIPT%" %*
)

:end
REM End the local scope to clean up environment variables
ENDLOCAL
