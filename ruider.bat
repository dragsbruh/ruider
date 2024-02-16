@echo off
SETLOCAL
SET SCRIPT=%~dp0\ruider.py

if "%*" == "" (
    goto invisibleoutput
)

if "%1" == "-d" (
    goto visibleoutput
)

if "%1" == "-w" (
    goto invisibleoutput
)

:invisibleoutput
pythonw "%SCRIPT%"
goto end

:visibleoutput
python "%SCRIPT%" "%*"

:end