# Earnings Calendar & Portfolio Analytics Platform

A production-ready starter monorepo for a professional earnings calendar and portfolio analytics web application.

## Stack
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts
- **Backend:** FastAPI, SQLAlchemy, Pydantic, JWT auth
- **Database:** PostgreSQL
- **Deployment:** Docker Compose

## Highlights
- Interactive earnings calendar by index/watchlist
- Security detail dashboard with valuation + analyst sentiment + earnings trend
- User auth and persisted portfolios (create/import/export)
- Scenario analytics (rates, inflation, sector shocks) with VaR and Sharpe
- Multi-provider earnings data service abstraction with fallback order

## Quick start
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

docker compose up --build
```

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

## API providers
Configured fallback chain:
1. Bloomberg Enterprise API (if licensed; connector placeholder)
2. Financial Modeling Prep
3. Polygon.io
4. Alpha Vantage
5. Yahoo Finance wrapper

Set credentials in `backend/.env`.

## Development
```bash
# backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend
cd frontend
npm install
npm run dev
```
