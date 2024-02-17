@echo off
SETLOCAL
SET SCRIPT=%~dp0\ruider.py

if "%*" == "" (
    goto invisibleoutput
)

if "%1" == "-v" (
    goto visibleoutput
)

if "%1" == "-i" (
    goto invisibleoutput
)

goto visibleoutput

:invisibleoutput
pythonw "%SCRIPT%"
goto end

:visibleoutput
python "%SCRIPT%" "%*"
goto end

:end