#!/usr/bin/env bash
set -euo pipefail
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Install Docker first." >&2
  exit 1
fi
docker build -t symptomx-app .
docker run -d -p 8000:8000 --name symptomx symptomx-app
echo "Running at http://127.0.0.1:8000"
