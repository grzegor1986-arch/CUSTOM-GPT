# LUMEN / SOTE v5.1 — FULL REAL REPO

Deploy-ready blueprint for a minimal SaaS with real payments:
- **Frontend** (Next.js)
- **Backend** (FastAPI)
- **Stripe checkout + webhook**
- **Railway + Vercel deploy helpers**

## Repo structure

```text
.
├── README.md
├── docker-compose.yml
├── .env.example
├── Makefile
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── health.py
│   │   └── payments.py
│   ├── services/
│   │   ├── stripe_service.py
│   │   └── revenue_tracker.py
│   └── deploy/
│       ├── railway.py
│       └── vercel.py
├── frontend/
│   ├── pages/
│   │   ├── index.tsx
│   │   └── success.tsx
│   ├── lib/
│   │   └── api.ts
│   └── package.json
└── scripts/
    └── deploy_all.sh
```

## 1) Environment setup

Copy `.env.example` to `.env` and fill your real values.

```bash
cp .env.example .env
```

Required keys:
- `STRIPE_SECRET_KEY`
- `STRIPE_PRICE_ID`
- `STRIPE_WEBHOOK_SECRET`
- `VERCEL_TOKEN`
- `RAILWAY_TOKEN`
- `NEXT_PUBLIC_API_URL`

## 2) Local run

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Or use Makefile:
```bash
make run
```

## 3) Core flow

1. User clicks **Buy Now** on frontend.
2. Frontend calls backend `/checkout`.
3. Backend creates Stripe Checkout session.
4. Stripe redirects to success page.
5. Stripe webhook calls backend `/webhook`.
6. Revenue event is tracked/logged.

## 4) Deploy

One-command pipeline:

```bash
make deploy
```

This runs `scripts/deploy_all.sh`, which:
- installs backend deps,
- builds frontend,
- calls Railway + Vercel deploy helpers.

## Domain flow example

- `ai-product.emyself.com` → frontend (Vercel)
- `api.emyself.com` → backend (Railway)

## Notes

- Deployment helper scripts are intentionally minimal; adjust payloads to your project IDs and infra setup.
- Add proper persistence/analytics before scaling (DB, queues, retries, idempotency).
