# Initial Implementation Guide

## Architecture
- **Frontend SPA (Next.js):**
  - Earnings calendar grid with collapsible daily events.
  - Security dashboard with valuation, consensus, and surprise trend chart.
  - Portfolio manager scaffold (create/edit holdings) ready for auth token wiring.
  - Scenario simulator for macro sensitivity and risk metrics.
- **Backend API (FastAPI):**
  - JWT auth (`/api/auth/signup`, `/api/auth/login`).
  - Market endpoints (`/api/market/earnings`, `/api/market/security/{ticker}`).
  - Portfolio endpoints (`/api/portfolio` CRUD/list, import/export CSV, scenario).
- **Persistence:** PostgreSQL via SQLAlchemy models for users, portfolios, holdings.
- **Provider fallback:** Bloomberg -> FMP -> Mock. Plug additional providers into `MarketDataService`.

## Data reliability and rate-limit strategy
- Provider abstraction isolates API quirks and enables fallback.
- Fail-fast requests with per-provider `httpx` timeout.
- Catch-and-continue behavior for resilient multi-provider retries.
- Mock fallback ensures UI remains usable during outages.

## Deployment checklist
1. Configure environment files from examples.
2. Add licensed Bloomberg connector if enterprise access exists.
3. Set production CORS origins and JWT secret.
4. Run DB migrations (Alembic recommended in next iteration).
5. Add background job queue for historical earnings backfill.

## Immediate next iteration priorities
1. Connect frontend portfolio manager to authenticated backend endpoints.
2. Add sector/market-cap controls in calendar UI and URL-state synchronization.
3. Add benchmark-relative performance charts and time-series return ingestion.
4. Add integration tests against real provider sandbox keys.
