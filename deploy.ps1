$ErrorActionPreference = "Stop"
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Write-Error "Docker is not installed. Install Docker Desktop first."
}
docker build -t symptomx-app .
docker run -d -p 8000:8000 --name symptomx symptomx-app
Write-Host "Running at http://127.0.0.1:8000"
