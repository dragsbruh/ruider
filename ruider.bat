@echo off
SETLOCAL
SET SCRIPT=%~dp0\ruider.py
pythonw "%SCRIPT%" %*
