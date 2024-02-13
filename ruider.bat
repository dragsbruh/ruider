@echo off
SETLOCAL
SET SCRIPT=%~dp0\ruider.py

if "%*" == "" (
	pythonw "%SCRIPT%"
    goto end
)

python "%SCRIPT%" "%*"

:end