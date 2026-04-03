# ABOUTME: Market API routes for earnings calendar and security overview queries.
# ABOUTME: Exposes filtered index/watchlist events and detailed company metrics.
from datetime import date

from fastapi import APIRouter

from app.schemas.market import EarningsEvent, SecurityOverview
from app.services.providers import MarketDataService

router = APIRouter(prefix="/api/market", tags=["market"])
service = MarketDataService()

INDEX_MEMBERS = {
    "sp500": ["AAPL", "MSFT", "AMZN", "NVDA", "JPM", "XOM", "GOOGL"],
    "nasdaq100": ["AAPL", "MSFT", "NVDA", "META", "TSLA", "AVGO"],
    "dow30": ["AAPL", "MSFT", "JPM", "V", "UNH", "GS"],
}


@router.get("/indices", response_model=dict[str, list[str]])
async def indices():
    return INDEX_MEMBERS


@router.get("/earnings", response_model=list[EarningsEvent])
async def earnings_calendar(
    index: str = "sp500",
    symbols: str | None = None,
    start: date | None = None,
    end: date | None = None,
    sector: str | None = None,
    min_market_cap: float | None = None,
):
    start_date = start or date.today()
    end_date = end or start_date
    ticker_list = symbols.split(",") if symbols else INDEX_MEMBERS.get(index.lower(), [])
    events = await service.earnings_calendar(ticker_list, start_date, end_date)
    if sector:
        events = [event for event in events if (event.sector or "").lower() == sector.lower()]
    if min_market_cap:
        events = [event for event in events if (event.market_cap or 0.0) >= min_market_cap]
    return events


@router.get("/security/{ticker}", response_model=SecurityOverview)
async def security_overview(ticker: str):
    return await service.security_overview(ticker.upper())
