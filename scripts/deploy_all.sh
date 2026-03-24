#!/bin/bash
set -euo pipefail

echo "🔥 STARTING FULL PIPELINE"

cd backend
pip install -r requirements.txt
uvicorn main:app --reload &
BACKEND_PID=$!
cd ../frontend
npm install
npm run build

echo "🚀 Deploying..."
cd ..
PYTHONPATH=backend python -c "from deploy.vercel import deploy_frontend; print(deploy_frontend())"
PYTHONPATH=backend python -c "from deploy.railway import deploy_backend; print(deploy_backend())"

kill "$BACKEND_PID" || true

echo "💸 LIVE"
