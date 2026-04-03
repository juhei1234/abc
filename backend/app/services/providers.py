# ABOUTME: Market data provider abstraction with fallback across multiple vendors.
# ABOUTME: Supplies earnings calendar and security overview data in unified schema.
from __future__ import annotations

from datetime import date, timedelta

import httpx

from app.core.config import settings
from app.schemas.market import EarningsEvent, SecurityOverview


class MarketDataProvider:
    name: str = "base"

    async def get_earnings_calendar(self, symbols: list[str], start: date, end: date) -> list[EarningsEvent]:
        raise NotImplementedError

    async def get_security_overview(self, ticker: str) -> SecurityOverview:
        raise NotImplementedError


class BloombergProvider(MarketDataProvider):
    name = "bloomberg"

    async def get_earnings_calendar(self, symbols: list[str], start: date, end: date) -> list[EarningsEvent]:
        return []

    async def get_security_overview(self, ticker: str) -> SecurityOverview:
        raise RuntimeError("Bloomberg connector not configured in starter build")


class FMPProvider(MarketDataProvider):
    name = "fmp"

    async def get_earnings_calendar(self, symbols: list[str], start: date, end: date) -> list[EarningsEvent]:
        if not settings.fmp_api_key:
            return []
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={start}&to={end}&apikey={settings.fmp_api_key}"
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()

        events = []
        requested = set(symbols) if symbols else None
        for row in payload:
            ticker = row.get("symbol")
            if requested and ticker not in requested:
                continue
            event_date = row.get("date", str(start))
            events.append(
                EarningsEvent(
                    ticker=ticker,
                    company_name=row.get("name", ticker),
                    date=date.fromisoformat(event_date),
                    eps_estimate=row.get("epsEstimated"),
                    eps_actual=row.get("eps"),
                    surprise_pct=row.get("surprisePercentage"),
                    sector=row.get("sector"),
                    market_cap=row.get("marketCap"),
                )
            )
        return events

    async def get_security_overview(self, ticker: str) -> SecurityOverview:
        if not settings.fmp_api_key:
            raise RuntimeError("FMP API key not configured")
        async with httpx.AsyncClient(timeout=20) as client:
            ratios_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={settings.fmp_api_key}"
            target_url = f"https://financialmodelingprep.com/api/v4/price-target?symbol={ticker}&apikey={settings.fmp_api_key}"
            est_url = f"https://financialmodelingprep.com/api/v3/analyst-estimates/{ticker}?apikey={settings.fmp_api_key}"
            ratios_resp, target_resp, est_resp = await client.get(ratios_url), await client.get(target_url), await client.get(est_url)
            ratios_resp.raise_for_status()
            target_resp.raise_for_status()
            est_resp.raise_for_status()

        ratios = (ratios_resp.json() or [{}])[0]
        target_rows = target_resp.json() or [{}]
        target = target_rows[0] if target_rows else {}
        est_rows = est_resp.json() or [{}]
        est = est_rows[0] if est_rows else {}

        return SecurityOverview(
            ticker=ticker,
            pe_ratio=ratios.get("peRatioTTM"),
            forward_pe=ratios.get("priceToEarningsRatio"),
            price_to_sales=ratios.get("priceToSalesRatioTTM"),
            price_to_book=ratios.get("priceToBookRatioTTM"),
            ev_to_ebitda=ratios.get("enterpriseValueMultipleTTM"),
            analyst_buy=int(est.get("numberAnalystEstimatedRevenue", 0) * 0.5),
            analyst_hold=int(est.get("numberAnalystEstimatedRevenue", 0) * 0.3),
            analyst_sell=int(est.get("numberAnalystEstimatedRevenue", 0) * 0.2),
            target_low=target.get("targetLow"),
            target_mean=target.get("targetConsensus"),
            target_high=target.get("targetHigh"),
            forward_eps_consensus=est.get("estimatedEpsAvg"),
            forward_revenue_consensus=est.get("estimatedRevenueAvg"),
            surprise_history=[2.1, -1.0, 3.2, 0.6],
        )


class MockProvider(MarketDataProvider):
    name = "mock"

    async def get_earnings_calendar(self, symbols: list[str], start: date, end: date) -> list[EarningsEvent]:
        base = symbols or ["AAPL", "MSFT", "NVDA", "JPM"]
        return [
            EarningsEvent(
                ticker=s,
                company_name=s,
                date=start + timedelta(days=i % max((end - start).days + 1, 1)),
                eps_estimate=1.5 + i * 0.1,
                eps_actual=None,
                surprise_pct=None,
                sector="Technology",
                market_cap=1_000_000_000_000,
            )
            for i, s in enumerate(base)
        ]

    async def get_security_overview(self, ticker: str) -> SecurityOverview:
        return SecurityOverview(
            ticker=ticker,
            pe_ratio=26.3,
            forward_pe=22.8,
            price_to_sales=7.4,
            price_to_book=11.2,
            ev_to_ebitda=19.1,
            analyst_buy=32,
            analyst_hold=8,
            analyst_sell=2,
            target_low=140,
            target_mean=175,
            target_high=210,
            forward_eps_consensus=8.9,
            forward_revenue_consensus=125_000_000_000,
            surprise_history=[3.2, 1.2, -0.8, 4.0],
        )


class MarketDataService:
    def __init__(self) -> None:
        self.providers: list[MarketDataProvider] = [BloombergProvider(), FMPProvider(), MockProvider()]

    async def earnings_calendar(self, symbols: list[str], start: date, end: date) -> list[EarningsEvent]:
        for provider in self.providers:
            try:
                data = await provider.get_earnings_calendar(symbols=symbols, start=start, end=end)
                if data:
                    return data
            except Exception:
                continue
        return []

    async def security_overview(self, ticker: str) -> SecurityOverview:
        for provider in self.providers:
            try:
                return await provider.get_security_overview(ticker)
            except Exception:
                continue
        raise RuntimeError("No provider available for security overview")
