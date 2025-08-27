param(
  [switch]$NoReload
)

$ErrorActionPreference = "Stop"
function Write-Section($msg) { Write-Host "=== $msg ===" -ForegroundColor Cyan }

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Section "Working directory: $here"

# venv paths
$venv = Join-Path $here "venv"
$venvPython = Join-Path $venv "Scripts\python.exe"

# Helper: find a system python
function Resolve-Python {
  $cmd = Get-Command python -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  $pyCmd = Get-Command py -ErrorAction SilentlyContinue
  if ($pyCmd) { return { param($args) & py -3 @args } }
  return $null
}

# Ensure venv
if (!(Test-Path $venvPython)) {
  Write-Section "Creating virtual environment at $venv ..."
  $pythonExe = Resolve-Python
  if ($null -eq $pythonExe) {
    Write-Error @"
No Python interpreter was found on PATH.

Install Python 3.9+ from https://www.python.org/downloads/
Check the box "Add python.exe to PATH" during install.
Then re-run: .\run.bat
"@
  }

  if ($pythonExe -is [scriptblock]) {
    & $pythonExe -m venv "$venv"
  } else {
    & "$pythonExe" -m venv "$venv"
  }
}

# Use venv python from here on
$python = $venvPython

Write-Section "Upgrading pip (best effort)"
& $python -m pip install --upgrade pip --timeout 60 --retries 2
if (-not $?) { Write-Warning "pip upgrade skipped (non-fatal)." }

Write-Section "Installing requirements"
& $python -m pip install -r (Join-Path $here "requirements.txt") --timeout 120 --retries 2

Write-Section "Starting API server at http://127.0.0.1:8000"
$reload = ""
if (-not $NoReload) { $reload = "--reload" }

& $python -m uvicorn backend.app:app $reload --log-level info
