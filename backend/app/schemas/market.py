# ABOUTME: Pydantic schemas for earnings calendar events and security detail views.
# ABOUTME: Standardizes provider-agnostic market data returned by backend services.
from datetime import date

from pydantic import BaseModel


class EarningsEvent(BaseModel):
    ticker: str
    company_name: str
    date: date
    eps_estimate: float | None
    eps_actual: float | None
    surprise_pct: float | None
    sector: str | None = None
    market_cap: float | None = None


class SecurityOverview(BaseModel):
    ticker: str
    pe_ratio: float | None
    forward_pe: float | None
    price_to_sales: float | None
    price_to_book: float | None
    ev_to_ebitda: float | None
    analyst_buy: int
    analyst_hold: int
    analyst_sell: int
    target_low: float | None
    target_mean: float | None
    target_high: float | None
    forward_eps_consensus: float | None
    forward_revenue_consensus: float | None
    surprise_history: list[float]
