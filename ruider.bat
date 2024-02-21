@REM TODO: Update this so much

@echo off
SETLOCAL
SET SCRIPT=%~dp0\launcher.py

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
pythonw "%SCRIPT%" %2
goto end

:visibleoutput
python "%SCRIPT%" %*
goto end

:end