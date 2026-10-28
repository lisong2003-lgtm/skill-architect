@echo off
setlocal
set "PY=%PYTHON%"
if "%PY%"=="" (py -3 >nul 2>&1 && set "PY=py -3") 
if "%PY%"=="" set "PY=python"
%PY% "%~dp0validate.py" %*
exit /b %ERRORLEVEL%
