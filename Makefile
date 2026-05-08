.PHONY: run deploy backend frontend

run: backend frontend

backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm install && npm run dev

deploy:
	bash scripts/deploy_all.sh
