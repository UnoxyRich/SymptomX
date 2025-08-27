@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%setup_and_run.ps1" %*
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo If you saw a policy error, open PowerShell and run:
  echo   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  echo Then double-click this file again.
  echo.
  pause
)
endlocal
